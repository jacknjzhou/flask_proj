#! coding:utf-8

from __future__ import absolute_import

import time
import functools
import traceback

from find_partner.celery import app
from find_partner import models as service
from find_partner import notify_models as n_service


@app.task
def rt_find_partner(company_id, company_name):
    """
    步骤1:
        根据企业id, 从tb_company_customer表中找出对应的rCompanyName列表;
        遍历rCompanyName列表, 并剔除没有tb_company_customer.companyName相对应的列表;
    步骤2:
        根据企业id, 从tb_company_vendor表中找出对应的rCompanyName列表;
        遍历rCompanyName列表, 并剔除没有tb_company_vendor.companyName相对应的列表;
    """

    session = service.create_partner_session()
    try:
        results = session.query(service.TbCompanyCustomer.rCompanyName). \
            filter(service.TbCompanyCustomer.companyId == company_id). \
            filter(service.TbCompanyCustomer.inviteStatus == 0). \
            all()

        _customer_filter_with_session = functools.partial(_customer_filter, session=session)
        _customer_map_with_session = functools.partial(_customer_map, session=session)
        results = map(_customer_map_with_session, filter(_customer_filter_with_session, results))

        _send_results(company_id, company_name, results, role='customer')

        # vendor process
        results = session.query(service.TbCompanyVendor.rCompanyName). \
            filter(service.TbCompanyVendor.companyId == company_id). \
            filter(service.TbCompanyVendor.inviteStatus == 0). \
            all()

        _vendor_filter_with_session = functools.partial(_vendor_filter, session=session)
        _vendor_map_with_session = functools.partial(_vendor_map, session=session)
        results = map(_vendor_map_with_session, filter(_vendor_filter_with_session, results))

        _send_results(company_id, company_name, results, role='vendor')

        msg = "ok"
    except:
        print traceback.format_exc()
        msg = "error"
    finally:
        session.close()

    return msg


def _send_results(company_id, company_name, results, role=None):
    if 0 == len(results):
        return

    results = map(lambda _tuple: dict(
        rCompanyId=_tuple[0],
        rCompanyName=_tuple[1],
        rContact=_tuple[2],
        rTel=_tuple[3]), results)

    print company_id, company_name, role, results
    session = n_service.create_notify_session()
    try:
        if 'customer' == role:
            for item in results:
                cc = n_service.TbCompanyRecmdRelation(
                    companyId=company_id,
                    companyName=company_name,
                    vendorOrCustomer='customer',
                    rCompanyId=item.get("rCompanyId", 0),
                    rCompanyName=item.get("rCompanyName", ""),
                    validFlag=1,
                    infoType="unset",
                    rContact=item.get("rContact", ""),
                    rTel=item.get("rTel", ""),
                    updateTime=int(time.time())
                )
                session.merge(cc)
                session.commit()

        elif 'vendor' == role:
            for item in results:
                cc = n_service.TbCompanyRecmdRelation(
                    companyId=company_id,
                    companyName=company_name,
                    vendorOrCustomer='vendor',
                    rCompanyId=item.get("rCompanyId", 0),
                    rCompanyName=item.get("rCompanyName", ""),
                    validFlag=1,
                    infoType="unset",
                    rContact=item.get("rContact", ""),
                    rTel=item.get("rTel", ""),
                    updateTime=int(time.time())
                )
                session.merge(cc)
                session.commit()
        else:
            pass
    except:
        print traceback.format_exc()
    finally:
        session.close()
    return


def _customer_map(item, session=None):
    ret = session.query(service.TbCompanyCustomer.companyId,
                        service.TbCompanyCustomer.contact,
                        service.TbCompanyCustomer.tel). \
        filter(service.TbCompanyCustomer.companyName == item[0]). \
        one_or_none()
    if not ret:
        ret = [None] * 3

    return ret[0], item[0], ret[1], ret[2]


def _customer_filter(item, session=None):
    ret = session.query(service.TbCompanyCustomer.companyName). \
        filter(service.TbCompanyCustomer.companyName == item[0]). \
        one_or_none()
    if ret:
        return True
    else:
        return False


def _vendor_filter(item, session=None):
    ret = session.query(service.TbCompanyVendor.companyName). \
        filter(service.TbCompanyVendor.companyName == item[0]). \
        one_or_none()
    if ret:
        return True
    else:
        return False


def _vendor_map(item, session=None):
    ret = session.query(service.TbCompanyVendor.companyId,
                        service.TbCompanyVendor.contact,
                        service.TbCompanyVendor.tel). \
        filter(service.TbCompanyVendor.companyName == item[0]). \
        one_or_none()
    if not ret:
        ret = [None] * 3

    return ret[0], item[0], ret[1], ret[2]


@app.task
def crontab_find_partners():
    """
    从tb_conf_center_company依次拿出企业, 找推荐关系
    @return: None
    """

    print 'crontab_find_partners begin.'
    session = service.create_partner_session()
    try:
        results = session.query(service.TbConfCenterCompany.companyId,
                                service.TbConfCenterCompany.companyName). \
            all()
        for company_id, company_name in results:
            rt_find_partner(company_id, company_name)
    except:
        print traceback.format_exc()
    finally:
        session.close()

    print 'crontab_find_partners end.'

    return
