#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

import dstracmd
from decimal import Decimal
from apscheduler.triggers.interval import IntervalTrigger, datetime
import datetime as dt
from models import *
import random
from utils import get_gmt_time_yyyymmddhhmmss, get_timestamp_daily_last_second
from itertools import groupby
import const
import logging
import useraddr


async def start_scan(scheduler):
    trigger = IntervalTrigger(start_date=datetime.now() + dt.timedelta(seconds=5), minutes=10)
    scheduler.add_job(__all_jobs, trigger, coalesce=True)
    # await __all_jobs()
    # l1 = [1, 2, 3, 4, 5]
    # l2 = [2, 3, 4]
    # l3 = [l1.remove(i) for i in l2]
    # print(l3)
    # print(random.randint(0, 0))
    # l1 = ['b', 'c', 'd', 'b', 'c', 'a', 'a']
    # l2 = sorted(set(l1), key=l1.index)
    # l1.extend(l2)
    # print(l1)
    # print(l1.index(a))
    # print(str(Decimal(1000000).__round__(10)))
    # INFO: root:  ###当前钱包数据:钱包币数:29255.60423, 未成熟币数:0, 前一条钱包数:24877.01433 ,能使用的分配总币数:29255.60423, 本次股份分配收益:44.99990
    # INFO: root:[stevenwong2017]
    # 前一条股份记录: 股份:0.438972040576532, 开始数额: 10920.31374389
    # INFO: root:[stevenwong2017]
    # 新股份记录: 开始数据:10940.06744182, 股份: 0.373947752225890, PoS利息: 19.75369793
    # INFO: root:[dumh]
    # 前一条股份记录: 股份:0.561027959423468, 开始数额: 13956.70058611
    # INFO: root:[dumh]
    # 新股份记录: 开始数据:13981.94678818, 股份: 0.477923705771339, PoS利息: 25.24620207
    # INFO: root:[Parker Lee]
    # 前一条股份记录: 股份:0, 开始数额: 0
    # INFO: root:[Parker Lee]
    # 新股份记录: 开始数据:4333.59000000, 股份: 0.148128542002771, PoS利息: 0E-8
    # getcontext().rounding = decimal.ROUND_HALF_UP
    # a = Decimal(str(10940.06744182))
    # d = Decimal(str(29255.60423))
    # print((a.__round__(7) / d).__round__(15))
    # print((a.__round__(3) / d.__round__(3)))
    # print((a.__round__(3) / d.__round__(3)).__round__(15))
    # 0.37394775222589
    # 0.3739477522259330891967019202
    # print(b/d)
    # print(c/d)
    # # 0.4779237057712959
    # # 0.37394775222593307
    # # 0.148128542002771
    # # 0.4779237057712959087292110254
    # # 0.3739477522259330891967019202


run_claim_tx = False


async def __all_jobs():
    await __scan_balance_job()
    await __process_immature_transactions()
    await __scan_transactions_job2()
    global run_claim_tx
    if not run_claim_tx:
        await __claim_tx()
        run_claim_tx = True
    # return
    # await __claim_tx_test()
    await __total_stakes_job()
    await __daily_pos_profit_job()


async def __claim_tx_test():
    # dumh 12319.44493000
    await DstInOutStake.updateByWhere('txid=?', ['d1a22903ea81ffaa0dfd1ef7e3878216c662a6587e14f06ef6ae49d0a2ba5f50'],
                                      userid='404504209241669642', username='dumh')
    # 村长 10500.00000000
    await DstInOutStake.updateByWhere('txid=?', ['73e9b4762f2167b185ade4a4b0f41e318825f4bb0cbc2b10c0a55f78b327331e'],
                                      userid='402631387577974797', username='stevenwong2017', isprocess=1)
    # 村长 39.00000000
    await DstInOutStake.updateByWhere('txid=?', ['17094b0375339fe17ff6df4100bc3aba1c149d7bc16445163885799b0979f0d1'],
                                      userid='402631387577974797', username='stevenwong2017', isprocess=1)
    # Parker Lee 4333.59000000
    await DstInOutStake.updateByWhere('txid=?', ['5c0ba1ea313d5327108598d1e554a7d9c737f80809a6c5b27a6095a529420e97'],
                                      userid='401916285929127947', username='Parker Lee', isprocess=0)
    # mako jr 7396.00000000
    await DstInOutStake.updateByWhere('txid=?', ['41b9edb5db88d9d7b0081108e4f05b20c1fd048d0e0143f03a724df72bc3d9d8'],
                                      userid='396837819550662668', username='mako jr', isprocess=1)
    # dumh 1178.57100000
    await DstInOutStake.updateByWhere('txid=?', ['56dc4454e6710aa71184b6456e7e7e0e44fb982e6a9469596289d78bd47901a1'],
                                      userid='404504209241669642', username='dumh')
    # cat Imao 7883.58000000
    await DstInOutStake.updateByWhere('txid=?', ['e9bc6891041464c2a66531116ec90cc75a9122bb07b2f2a3a1d848ed5ca033d8'],
                                      userid='411932460344016896', username='cat Imao', isprocess=1)
    # lucky168 649.00000000
    await DstInOutStake.updateByWhere('txid=?', ['9795560b3281f1151acc64596a534912f6c79248c032932204c2809f38abd751'],
                                      userid='407552893806182411', username='lucky168', isprocess=0)
    # baobao 649.00000000
    await DstInOutStake.updateByWhere('txid=?', ['56883f7dd4325c5c54e200e62ea6b5a79ff41319a81a15fb65ca5d303475e679'],
                                      userid='403478549379678211', username='baobao', isprocess=0)
    # Parker Lee 15.00000000
    await DstInOutStake.updateByWhere('txid=?', ['68cdcae5f26a94c2d2ab4502740ba411b37c82263014a46716c4a0696675e019'],
                                      userid='401916285929127947', username='Parker Lee', isprocess=0)
    # JWKY 1000.00000000
    await DstInOutStake.updateByWhere('txid=?', ['b47aae02d249fe4308e70c3a41ab787c7cc49f821e5e619fadbdf4c6dd0c06e7'],
                                      userid='403341228176965633', username='JWKY', isprocess=0)
    # dumh 2.00000000
    await DstInOutStake.updateByWhere('txid=?', ['4679e8a31331144ebd3bf50e80453a741eaf5c560571e103790a4b6d4488526f'],
                                      userid='404504209241669642', username='dumh')
    # dumh ﻿1902.137903
    await DstInOutStake.updateByWhere('txid=?', ['ae515f8d3829f7f4632519362285e961b7825c10885771fdc0f4922b5c706bef'],
                                      userid='404504209241669642', username='dumh')
    # Parker Lee ﻿431.3013
    await DstInOutStake.updateByWhere('txid=?', ['43c326304210a4a7e59a72ecb9a3bca5ad86d5b757e3c4a1d9b76fabb44851d8'],
                                      userid='401916285929127947', username='Parker Lee')


claim_txs = [
    # 12319.44493000
    # ['d1a22903ea81ffaa0dfd1ef7e3878216c662a6587e14f06ef6ae49d0a2ba5f50', '404504209241669642', 'dumh'],
    # 1178.57100000
    # ['56dc4454e6710aa71184b6456e7e7e0e44fb982e6a9469596289d78bd47901a1', '404504209241669642', 'dumh'],
    # 15
    # ['7ec64c31b5babb6ba6911d50d8fb36cbf93791afb49e9164ea207578adbcea0e', '404504209241669642', 'dumh'],
    # 2.00000000
    # ['4679e8a31331144ebd3bf50e80453a741eaf5c560571e103790a4b6d4488526f', '404504209241669642', 'dumh'],
    # 10.00000000
    # ['1210c38c31b53dd6923ffe35b9a7ab9ce40cee83564d3ac5568b9771e0202fd6', '404504209241669642', 'dumh'],
    # 1902.137903
    # ['ae515f8d3829f7f4632519362285e961b7825c10885771fdc0f4922b5c706bef', '404504209241669642', 'dumh'],
    # 2
    # ['69ad4f59ed1ebddf06a0a9567e1b089a6136efb568e9ed8a1b7f8bad7dde9dc4', '404504209241669642', 'dumh'],
    # 1695.61
    # ['8205e4c68713aa2e1d7c84ec918357e7bf5942ed76c54002cca6d7ce3e075802', '404504209241669642', 'dumh'],
    # ﻿1649.83
    # ['90c9584da3a64c228957277aeb7b3ff44c19df852f3149b9d27f8ca106675331', '404504209241669642', 'dumh'],
    # -1366.5001
    ['4b6478b66ff705a26730673cb0851ce0b2401bdd116645948c9ee0fd80fce0ea', '404504209241669642', 'dumh'],
    # 11
    # ['f6ea8c8bc7a57ee73980c28c77cfeac4031ba6a997d28b9ea2f906ef4d394948', '404504209241669642', 'dumh'],

    # '10500.00000000'
    # ['73e9b4762f2167b185ade4a4b0f41e318825f4bb0cbc2b10c0a55f78b327331e', '402631387577974797', 'stevenwong2017'],
    # '39.00000000'
    # ['17094b0375339fe17ff6df4100bc3aba1c149d7bc16445163885799b0979f0d1', '402631387577974797', 'stevenwong2017'],

    # 4333.59000000
    # ['5c0ba1ea313d5327108598d1e554a7d9c737f80809a6c5b27a6095a529420e97', '401916285929127947', 'Parker Lee'],
    # 15.00000000
    # ['68cdcae5f26a94c2d2ab4502740ba411b37c82263014a46716c4a0696675e019', '401916285929127947', 'Parker Lee'],
    # 431.3013
    # ['43c326304210a4a7e59a72ecb9a3bca5ad86d5b757e3c4a1d9b76fabb44851d8', '401916285929127947', 'Parker Lee'],
    # ﻿1157.00
    # ['05873b907800917ab331cb9c866a75d388dfb07d11d2b3999bf1841c08de50e7', '401916285929127947', 'Parker Lee'],
    # ﻿1336.00
    # ['f00a88842f276916aba9a4c5a05a398f9c0dc2e39584a859b26e245fec769d70', '401916285929127947', 'Parker Lee'],
    # 79.0- 补的
    ['2ad1eb01c693097cabe414b5e30f398ff5b518913c53bb1e286a91380433b1b2', '401916285929127947', 'Parker Lee'],

    # '7396.00000000'
    # ['41b9edb5db88d9d7b0081108e4f05b20c1fd048d0e0143f03a724df72bc3d9d8', '396837819550662668', 'mako jr'],
    # '2946.00'
    # ['6a2c17e7322f8609cb209252d134ab153a43f0126645a08282f94ba45e1b7372', '396837819550662668', 'mako jr'],
    # '466.6' --补的
    ['4c1bd75846b37cbee918fad533abc0098eb8bf110d8beaf2e177ed17a1bf3167', '396837819550662668', 'mako jr'],

    # '7883.58000000'
    # ['e9bc6891041464c2a66531116ec90cc75a9122bb07b2f2a3a1d848ed5ca033d8', '411932460344016896', 'cat Imao'],
    # 1194.108679
    # ['c7feaeb850fdfb409a2f9246cc74a7a0c67de1d80e7801861ed6664d4118128f', '411932460344016896', 'cat Imao'],
    # 281 --补的
    ['235eedd34d78dc6be288c421748aa34467c1eca23cc74db94144e3a7d9c31691', '411932460344016896', 'cat lmao'],
    # 1670.8

    # '649.00000000'
    # ['9795560b3281f1151acc64596a534912f6c79248c032932204c2809f38abd751', '407552893806182411', 'lucky168'],
    # lucky168 1200.00000000
    # ['1e9eb0a9f1def2068b120b8d35b3e565ed9011a5574b39253098823bfa4050b5', '407552893806182411', 'lucky168'],
    # 326.2 --补的
    ['63e6f6494ce036bbbbfd7361dee335dab39341f8cc683fae2a93c9e297955022', '407552893806182411', 'lucky168'],

    # '649.00000000'
    # ['56883f7dd4325c5c54e200e62ea6b5a79ff41319a81a15fb65ca5d303475e679', '403478549379678211', 'baobao'],
    # baobao 2000.00000000
    # ['77882a1d20a342dbd714ee0f4fd4764fc915ebbc2c1edaaa2d2b22908ce86c15', '403478549379678211', 'baobao'],
    # baobao -2880.0001
    # ['5af46fe0d6602074f6b960851a4b54351fa076651d7a96ad0b014e77bf342018', '403478549379678211', 'baobao'],
    # 213.64 --补的
    ['42624cc45d5599c9dc79d315d90f458666e55c0d4cd5fcdc1f33de1dbb576ec3', '403478549379678211', 'baobao'],

    # JWKY '1000.00000000'
    # ['b47aae02d249fe4308e70c3a41ab787c7cc49f821e5e619fadbdf4c6dd0c06e7', '403341228176965633', 'JWKY'],

    # Ray '8363.6129351'
    # ['6494c6df7c2b975c2a59973b16397de0a0f173bedaf26669ce71ffaf3f79029c', '385061500034875392', 'Ray'],
]


async def __claim_tx():
    global claim_txs
    for tx in claim_txs:
        await DstInOutStake.updateByWhere('txid=?', [tx[0]], userid=tx[1], username=tx[2])


async def __scan_balance_job():
    get_info = dstracmd.getinfo()
    # now_time_fix_offset = int(time.time()) + get_info.timeoffset
    block_last_time = dstracmd.getbestblock().time
    logging.info('######: update time:{}({})'.format(block_last_time, get_gmt_time_yyyymmddhhmmss(block_last_time)))
    await DstWalletInfo(id=1, balance=get_info.balance, stake=get_info.stake, blocks=get_info.blocks,
                        update_at=block_last_time,
                        update_at_str=get_gmt_time_yyyymmddhhmmss(block_last_time)).replace()

    # walletBalance = await DstWalletBalance.find(1)
    # if walletBalance is None:
    #     walletBalance = DstWalletBalance(id=1, balance=get_info.balance, stake=get_info.stake,
    #                                      update_at=block_last_time,
    #                                      update_at_st=get_gmt_time_yyyymmddhhmmss(block_last_time))
    #     await walletBalance.save()
    # else:
    #     logging.info("before: WalletBalance:%s[%s]" % (
    #         walletBalance, time.strftime("%y-%m-%d %H:%M:%S", time.localtime(walletBalance.created_at))))
    # walletBalance.balance = get_info.balance
    # walletBalance.stake = get_info.stake
    # walletBalance.update_at = block_last_time
    # walletBalance.update_at_str = get_gmt_time_yyyymmddhhmmss(block_last_time)
    # await walletBalance.update()
    # logging.info("after: WalletBalance:%s[%s]" % (
    #     walletBalance, time.strftime("%y-%m-%d %H:%M:%S", time.localtime(walletBalance.created_at))))


def __get_transactions_count():
    start, step, count = 0, 100, 0
    start_txid = ''
    while True:
        txs = dstracmd.listtransactions(1, 0)
        if len(txs) == 0:
            return 0
        if start_txid != txs[0].txid:
            start = 0
            count = 0
            start_txid = txs[0].txid
        transactions = dstracmd.listtransactions(step, start)
        _count = len(transactions)
        if _count == 0:
            return count
        start += _count
        count += _count


def __get_index_count_by_txid(txid=''):
    """
    :param txid:
    :return: index 从零开始, count 总交易数
    """
    start, step, index, real_index, count = 0, 100, -1, -1, 0
    find = False
    find_index = -1
    start_txid = ''
    while True:

        # 检查在处理过程中链是否有变化,如果有,重新计算.
        txs = dstracmd.listtransactions(1, 0)
        if len(txs) == 0:
            return -1, 0
        if start_txid != txs[0].txid:
            start = 0
            count = 0
            index = -1
            find_index = -1
            find = False
            start_txid = txs[0].txid

        transactions = dstracmd.listtransactions(step, start)
        _count = len(transactions)
        if _count == 0:
            return find_index, count
        if not find:
            for t in transactions:
                index += 1
                real_index = start + _count - index % step - 1
                if t.txid == txid:
                    if find_index == -1:
                        find_index = real_index
                        # print("first:", find_index)
                    else:
                        find_index = real_index
                        # print("second:", find_index)
                        find = True
                        break
                    # print(real_index)
                elif find_index != -1 and real_index - find_index < 0:
                    find = True
                    break
        start += _count
        count += _count


async def __process_immature_transactions():
    """
    修正数据中immature状态的tx交易
    :return:
    """
    # await DstInOutStake.updateByWhere('`pos_time`>=? and isonchain=?',
    #                                   [1, 1], isprocess=0, stake=0, start_amount=0, pos_profit=0,
    #                                   start_balance=0, stage_pos_profit=0)
    # await DstInOutStake.deleteByWhere('`pos_time`>=? and isonchain=?', [1, 0])
    # await DstDailyProfit.deleteByWhere('profit_time>=?', [1])
    transactions = await DstTransactions.findAll("`category`=?", [const.CATEGORY_IMMATURE])
    if len(transactions):
        changedTx = []
        for t in transactions:
            tx_in_black = dstracmd.gettransaction(t.txid)
            if len(tx_in_black.details) == 0:
                await t.remove()
                changedTx.append(t)
            elif tx_in_black.details[0]['category'] == const.CATEGORY_GENERATE:
                t.category = const.CATEGORY_GENERATE
                await t.update()
            #
            # elif tx_in_black.confirmations > const.POS_NO_CONFLICTED_CONFIRMATIONS:
            #     t.category = const.CATEGORY_GENERATE
            #     await t.update()
            # 因为之前的处理逻辑中immature的数据是已经含包在, 所以只要更新可以了.
            # changedTx.append(t)
        # 如果有更改就重置这个时间后的股份信息, 并删除每天收益表里的数据
        if len(changedTx):
            min_tx = min(changedTx, key=lambda tx: tx.txtime)
            await DstInOutStake.updateByWhere('`pos_time`>=? and isonchain=?',
                                              [min_tx.txtime, 1], isprocess=0, stake=0, start_amount=0, pos_profit=0,
                                              start_balance=0, stage_pos_profit=0)
            await DstInOutStake.deleteByWhere('`pos_time`>=? and isonchain=?', [min_tx.txtime, 0])
            await DstDailyProfit.deleteByWhere('profit_time>=?', [min_tx.txtime])


if __name__ == '__main__':
    # _txs = dstracmd.listtransactions(400, 0)
    # a_count = len(_txs)
    # _i = a_count
    # for _t in _txs:
    #     _i = _i - 1
    #     print('%4d' % _i, _t.txid, _t.amount, _t.category)
    #     if _i == a_count - 25:
    #         break
    #
    # _index, a_count = __get_index_count_by_txid('9e017a2ba159cd6f2dcb99182c3fb480d3d23ebdedad7e6f4c3f61b2c374dd19')
    # print(_index, a_count)
    #
    # print(1 in (1, 2, 3, 4))
    print(time.time())
    gmt_time = time.gmtime(time.time())
    str_time = time.strftime("%Y-%m-%d %H:%M:%S", gmt_time)
    print(str_time)


def __log_tx(index, tx):
    logging.info('{:3}. {} {} {}'.format(index, tx.txid, tx.amount, tx.category))


async def __process_staking_info(txid):
    tx_detail = dstracmd.gettransaction(txid)
    for vin in tx_detail.vin:
        vin_tx_id = vin['txid']
        vin_vout = vin['vout']
        tx_vin = dstracmd.gettransaction(vin_tx_id)
        tx_vin_time = tx_vin.blocktime
        staking_time = tx_detail.blocktime
        wait_time = staking_time - tx_vin_time
        tx_vin_time_d = dt.datetime.utcfromtimestamp(tx_vin_time)
        staking_time_d = dt.datetime.utcfromtimestamp(staking_time)
        wait_time_d = staking_time_d - tx_vin_time_d
        wait_time_str = utils.get_time_days_hhmmss(wait_time_d.days, wait_time_d.seconds)
        vin_amount = tx_vin.vout[vin_vout]['value']
        unspent = DstStakingInfo(txid=txid, vin_txid=vin_tx_id, vin_vout=vin_vout, vin_amount=vin_amount,
                                 vin_tx_time=tx_vin_time, vin_tx_time_str=get_gmt_time_yyyymmddhhmmss(tx_vin_time),
                                 staking_time=staking_time, staking_time_str=get_gmt_time_yyyymmddhhmmss(staking_time),
                                 wait_time=wait_time, wait_time_str=wait_time_str)

        unspent_dbs = await DstStakingInfo.findAll('vin_txid=? and vin_vout=?', [vin_tx_id, vin_vout])
        if len(unspent_dbs) == 1:
            # 出现这种情况是由于冲突引起的
            conflicted_tx = unspent_dbs[0]
            logging.info(
                "######:conflicted: txid:{}, vin_txid:{}, vin_vout:{}".format(conflicted_tx.txid, vin_tx_id, vin_vout))
            await conflicted_tx.remove()
            # await unspent.update()
        # else:
        await unspent.save()


async def __scan_transactions_job2():
    last_db_tx = None
    transactions = await DstTransactions.findAll(orderBy="txtime DESC", limit=1)
    if len(transactions) != 0:
        last_db_tx = transactions[0]
    if last_db_tx is None:
        start_index, count = __get_index_count_by_txid('')
        # oldest transaction
        last_chain_tx = dstracmd.listtransactions(1, count - 1)[0]
        logging.info('oldest_txid:{}'.format(last_chain_tx.txid))
        # the oldest write to db
        txtime = last_chain_tx.blocktime
        if last_chain_tx.txid in const.POS_EFFECTIVE_AT_ONCE_TXID:
            pos_time = txtime
        else:
            pos_time = txtime + const.POS_EFFECTIVE_TIME
        await DstInOutStake(change_amount=last_chain_tx.amount, txid=last_chain_tx.txid,
                            userid='404504209241669642', username='dumh',
                            txtime=txtime,
                            txtime_str=get_gmt_time_yyyymmddhhmmss(txtime),
                            pos_time=pos_time,
                            pos_time_str=get_gmt_time_yyyymmddhhmmss(pos_time),
                            isprocess=False, isonchain=True,
                            change_username='', comment='deposit coin').save()
        last_db_tx = DstTransactions(txid=last_chain_tx.txid, idx=0, category=last_chain_tx.category,
                                     amount=last_chain_tx.amount,
                                     txtime=txtime,
                                     txtime_str=get_gmt_time_yyyymmddhhmmss(txtime))
        await last_db_tx.save()
        # await DstTransactions(txid=last_chain_tx.txid, idx=0, category=last_chain_tx.category,
        #                       amount=last_chain_tx.amount,
        #                       txtime=txtime,
        #                       txtime_str=get_gmt_time_yyyymmddhhmmss(txtime)).save()
        # last_process_txid = last_chain_tx.txid

    step = 50
    final_page = False
    while not final_page:
        logging.info('### last_process_txid:{}'.format(last_db_tx.txid))
        start_index, count = __get_index_count_by_txid(last_db_tx.txid)
        logging.info("### fix before:start_index:{},count,{}".format(start_index, count))
        # if count == 0 or start_index == 0:
        if count == 0:
            return
        # 计算从区块链上获取数据的开始位置, 及结束位置
        # if start_index == -1:
        # 当数据库中没有数据的时候, 返回-1,这个时候从链最开始进行处理
        # start_index = count - step
        # else:
        # 中间处理的加上上一批次最后处理的, 用于检验是否完整的链
        start_index -= (step - 1)
        if start_index <= 0:
            # 最新页的处理方式
            step += start_index
            start_index = 0
            final_page = True

        txs = dstracmd.listtransactions(step, start_index)
        txs_count = len(txs)
        logging.info(
            '### fix after:step:{}, start_index:{}, len(txs):{}, count:{}\n'.format(step, start_index, txs_count,
                                                                                    count))

        if txs_count > 6:
            __log_tx(start_index + txs_count - 1, txs[0])
            __log_tx(start_index + txs_count - 2, txs[1])
            __log_tx(start_index + txs_count - 3, txs[2])
            logging.info('.................')
            __log_tx(start_index + 2, txs[-3])
            __log_tx(start_index + 1, txs[-2])
            __log_tx(start_index, txs[-1])
        else:
            for index, t in enumerate(txs):
                __log_tx(start_index + txs_count - index - 1, t)

        last_chain_tx = txs[0]
        if last_db_tx.txid != last_chain_tx.txid:
            raise Exception("tx chain error: last:[%s], chain first:[%s]" % (last_db_tx.txid, last_chain_tx.txid))

        tx_ids = []
        for index, tx in enumerate(txs[1:], 1):
            tx_id = tx.txid
            if tx_id in tx_ids:
                continue
            tx_ids.append(tx_id)
            idx = count - (start_index + txs_count) + index
            txtime = tx.blocktime
            # 修正两个txtime一样引起的算占比时的错误
            logging.info("###############################:{},{}".format(txtime, last_db_tx.txtime))
            if txtime == last_db_tx.txtime:
                txtime += 1
            elif txtime + 1 == last_db_tx.txtime:
                txtime += 2

            last_db_tx = DstTransactions(txid=tx_id, idx=idx, category=tx.category, amount=tx.amount, txtime=txtime,
                                         txtime_str=get_gmt_time_yyyymmddhhmmss(txtime))
            if tx.category == const.CATEGORY_GENERATE or tx.category == const.CATEGORY_IMMATURE:
                pass
                # await tx_db.save()
                # await __process_staking_info(tx_id)
            # elif tx.txid in const.POS_RECEIVE_2_GENERATE:
            #     last_db_tx.category = const.CATEGORY_GENERATE
            else:
                category, tx_amount, userid, username = __analyze_tx(tx.txid)
                last_db_tx.amount = tx_amount
                last_db_tx.category = category
                if category == const.CATEGORY_SEND or category == const.CATEGORY_RECEIVE:
                    if category == const.CATEGORY_RECEIVE:
                        if tx_id in const.POS_EFFECTIVE_AT_ONCE_TXID:
                            pos_time = txtime
                        else:
                            pos_time = txtime + const.POS_EFFECTIVE_TIME
                        comment = 'deposit coin'
                    else:
                        pos_time = txtime
                        comment = 'withdraw coin'
                    await DstInOutStake(change_amount=tx_amount, txid=tx_id, userid=userid, username=username,
                                        txtime=txtime,
                                        txtime_str=get_gmt_time_yyyymmddhhmmss(txtime),
                                        pos_time=pos_time,
                                        pos_time_str=get_gmt_time_yyyymmddhhmmss(pos_time),
                                        isprocess=False, isonchain=True, change_username='',
                                        comment=comment).save()
            await last_db_tx.save()

            #     tx_in_chain = dstracmd.gettransaction(tx.txid)
            #     tx_amount = tx_in_chain.amount
            #     tx_fee = tx_in_chain.get('fee')
            #     if tx_fee is None or tx_amount < 0:
            #         # 如果不包含fee就是从别人那里收到的, 如果amount<0是发出去的, 也要要记录占比
            #         if tx_amount < 0:
            #             last_db_tx.category = const.CATEGORY_SEND
            #             tx_amount = Decimal(str(tx_amount)) + Decimal(str(tx_fee))
            #             last_db_tx.amount = tx_amount
            #             pos_time = txtime
            #             comment = 'withdraw coin'
            #         else:
            #             last_db_tx.category = const.CATEGORY_RECEIVE
            #             if tx_id in const.POS_EFFECTIVE_AT_ONCE_TXID:
            #                 pos_time = txtime
            #             else:
            #                 pos_time = txtime + const.POS_EFFECTIVE_TIME
            #             comment = 'deposit coin'
            #
            #         await DstInOutStake(change_amount=tx_amount, txid=tx_id,
            #                             txtime=txtime,
            #                             txtime_str=get_gmt_time_yyyymmddhhmmss(txtime),
            #                             pos_time=pos_time,
            #                             pos_time_str=get_gmt_time_yyyymmddhhmmss(pos_time),
            #                             isprocess=False, isonchain=True, change_username='',
            #                             comment=comment).save()
            #     elif tx_amount == 0:
            #         # 这种是split时产生的费用
            #         last_db_tx.amount = tx_fee
            #         last_db_tx.category = const.CATEGORY_SENDTOSELF
            # await last_db_tx.save()


# 返回 category,amount
def __analyze_tx(txid):
    tx_org = dstracmd.gettransaction(txid)
    # 这个变量只在发给自己或发出去的时候有用
    vin_sum_amount = Decimal("0")
    vin_address_is_all_airdrop = True
    vin_addresses = []
    for vin in tx_org.vin:
        vin_txid = vin['txid']
        vin_vout = vin['vout']
        tx_vin = dstracmd.gettransaction(vin_txid)
        tx_vin_vout = tx_vin.vout[vin_vout]
        vin_address = tx_vin_vout['scriptPubKey']['addresses'][0]
        vin_addresses.append(vin_address)
        vin_address_is_all_airdrop = vin_address_is_all_airdrop and (
                vin_address == const.POS_ADDRESS)
        vin_sum_amount += Decimal(str(tx_vin_vout['value']))

    vout_sum_amount = Decimal("0")
    vout_address_is_all_airdrop = True
    vout_addresses = []
    for vout in tx_org.vout:
        vout_address = vout['scriptPubKey']['addresses'][0]
        vout_addresses.append(vout_address)
        is_airdrop_address = const.POS_ADDRESS == vout_address
        vout_address_is_all_airdrop = vout_address_is_all_airdrop and is_airdrop_address
        if is_airdrop_address:
            vout_sum_amount += Decimal(str(vout['value']))

    if vin_address_is_all_airdrop:
        amount = float(vout_sum_amount - vin_sum_amount)
        if vout_address_is_all_airdrop:
            return const.CATEGORY_SENDTOSELF, amount, '', ''
        else:
            userid, username = __get_userid_username(vout_addresses)
            return const.CATEGORY_SEND, amount, userid, username
    else:
        userid, username = __get_userid_username(vin_addresses)
        return const.CATEGORY_RECEIVE, float(vout_sum_amount), userid, username


def __get_userid_username(addresses):
    userid = const.POS_NOUSER_ID
    username = const.POS_NOUSER_NAME
    for address in addresses:
        _user_addr = useraddr.get(address)
        if _user_addr is not None:
            userid = _user_addr.userid
            username = _user_addr.username
            break
    return userid, username


async def __total_stakes_job():
    '''
        股份计算job
    :return:
    '''
    # get_info = dstracmd.getinfo()
    # now_time_fix_offset = int(time.time()) + get_info.timeoffset
    block_last_time = dstracmd.getbestblock().time
    dst_in_out_stake_tx = await DstInOutStake.findAll('`isprocess`=? and `isonchain`=?', [0, 1], orderBy='pos_time')
    if len(dst_in_out_stake_tx) <= 0:
        return
    min_tx_in_chain = min(dst_in_out_stake_tx, key=lambda x: x.pos_time)
    dst_in_out_stake_tx.sort(key=lambda x: x.userid)
    dst_in_out_tx_group = groupby(dst_in_out_stake_tx, key=lambda x: x.userid)
    for k, v in dst_in_out_tx_group:
        min_tx = min(v, key=lambda x: x.pos_time)
        min_tx_pos_time = min_tx.pos_time
        # 检查需要处理的最小的记录有没有已经处理的数据, 如果有,将数据重置
        had_processed_count = await DstInOutStake.findNumber('count(`id`)',
                                                             '`pos_time` >= ? and `isprocess`=?',
                                                             [min_tx_pos_time, 1])
        # had_processed_tx = await DstInOutStake.findAll(
        #     '`pos_time` > ? and `isprocess`=? and `isonchain`=?', [min_tx_pos_time, 1, 1], limit=1)
        if had_processed_count > 0:
            # 删除本条tx相关用户和nouseid有效时间前的分发记录
            await DstInOutStake.deleteByWhere('`pos_time`>=? and `isonchain`=? and (`userid`=? or `userid`=?)',
                                              [min_tx_pos_time, 0, k, const.POS_NOUSER_ID])

            # 把本条有效时间前的已经处理过的数据重置成未处理,包括本用户和nouseid记录
            await DstInOutStake.updateByWhere('`pos_time`>? and (`userid`=? or `userid`=?)',
                                              [min_tx_pos_time, k, const.POS_NOUSER_ID],
                                              isprocess=0, stake=0, start_amount=0, pos_profit=0, start_balance=0,
                                              stage_pos_profit=0)
            # 删除每天结算报表中包括本条之前的数据
            await DstDailyProfit.deleteByWhere('`pos_time`>=?', [min_tx_pos_time])

    now_time = block_last_time
    # now_time = 1523254655
    # 获取待处理的记录 不根据isprocess来获取,是因为如果一条交易记录在链的中间获取,之后的分配将计算不了.
    # 即只要链的中间有没有处理过的, 从这个记录开始之后的除了已经认领的, 其他的都要重新计算, 包括nouseid
    dst_in_out_stake_tx = await DstInOutStake.findAll('`isonchain`=? and `pos_time`<=? and `pos_time` >= ?',
                                                      [1, now_time, min_tx_in_chain.pos_time], orderBy='pos_time')

    # 获取要处理数据的前一条记录
    prev_tx = await DstInOutStake.findAll('`pos_time`<? and isonchain=?', [min_tx_in_chain.pos_time, 1],
                                          orderBy='`pos_time` desc', limit=1)
    if prev_tx:
        prev_tx = prev_tx[0]

    # 获取需要处理的用户ID 不可以用, 因为如果是最新添加的, 其他的用户获取不了.
    # wait_process_userids = {tx.userid for tx in dst_in_out_stake_tx}
    count = 0
    for tx in dst_in_out_stake_tx:
        # 每次都要操作nouserid这个账户,来对未认领的交易记录进行计算,以保证已经计算好的数据的正确性.
        # 首先获取启用时间之前表里这条tx相关用户最后一条已处理记录,根据启用时间来获取
        # 如果没有获取到, 之前的数量为零, 如果有获取到, 计算从上次分配股份到现在的获利, 加入到这个表中, 此时还要计算之前所有人的股权利息
        # 如果已经存在, 则不操作, 如果没有存在, 则新加入.
        # 在程序处理完之后, 所有用户股份分配的最后时间必须是一至的,即最后进行股分分配的tx的时间
        pos_time = tx.pos_time

        current_tx_userid = tx.userid
        current_tx_username = tx.username
        change_amount = Decimal(str(tx.change_amount))
        # 获取处理时的钱包总额, 要包含这个时间之前的钱包数量, 因为这是根据成熟时间来算的, 这个成熟时间在交易链上可能不存在.
        wallet_balance = await DstTransactions.findNumber('sum(`amount`)', '`txtime`<=?',
                                                          [pos_time])
        wallet_balance = Decimal(str(wallet_balance))
        # 获取本次时间段之间不能参与占比分配的币的总量
        immature_amount = (await DstInOutStake.findNumber('sum(`change_amount`)',
                                                          '`txtime`< ? and `pos_time`> ? and isonchain = ?',
                                                          [pos_time, pos_time, 1]) or 0)
        immature_amount = Decimal(str(immature_amount))

        # 本次分配钱包真正的开始总额
        mature_balance = wallet_balance - immature_amount

        # 获取本次分配到上次分配时间段里钱包的收入---------
        # 获取前一条tx钱包的总数

        prev_balance = 0
        if len(prev_tx):
            prev_balance = Decimal(str(prev_tx.start_balance))
            stage_pos_profit = (mature_balance - prev_balance - change_amount)
        else:
            stage_pos_profit = Decimal(0)

        # stage_pos_profit2 = await  DstInOutStake.findNumber('sum(amount)', '`txtime`')
        # 钱包收入

        # 获取本次处理交易时间段时钱包的收入---------

        logging.info('-----------------------------------------------------------------')
        logging.info('###当前钱包数据:钱包币数:%s, 未成熟币数:%s, 前一条钱包数:%s ,能使用的分配总币数:%s, 本次股份分配收益:%s', wallet_balance,
                     immature_amount, prev_balance, mature_balance, stage_pos_profit)

        # 所有需要处理的用户
        wait_process_users_1 = await DstInOutStake.findDistinct(['userid', 'username'],
                                                                'pos_time<=?', [pos_time])
        # 当前时间线上已经处理的用户
        wait_process_users = (await DstInOutStake.findDistinct(['userid', 'username'],
                                                               'pos_time=? and isprocess=?', [pos_time, 1]) or [])
        # 删除已经处理的用户,留下未处理的用户
        for user in wait_process_users:
            wait_process_users_1.remove(user)
        if len(wait_process_users_1) == 0:
            random_index = random.randint(0, len(wait_process_users) - 1)
            fix_user = wait_process_users[random_index]
            wait_process_users.pop(random_index)
            wait_process_users.append(fix_user)
        else:
            random_index = random.randint(0, len(wait_process_users_1) - 1)
            fix_user = wait_process_users_1[random_index]
            wait_process_users_1.pop(random_index)
            wait_process_users_1.append(fix_user)
            wait_process_users.extend(wait_process_users_1)
        user_index = 0
        user_count = len(wait_process_users)
        processed_sum_stake = Decimal(0).__round__(const.PREC_STAKE)
        processed_sum_pos_profit = Decimal(0).__round__(const.PREC_BALANCE)
        logging.info("############################:current:{}, fix user:{}, user_count:{}".format(current_tx_username,
                                                                                                  fix_user[1],
                                                                                                  user_count))
        for userid, username in wait_process_users:
            logging.info("############################:当前待处理用户:|{}|,[{}]".format(username, userid))
            user_index += 1
            # 获取该用户前二条股份的数据,如果其他用户第一条数据的pos_time和主链上的一样, 则不处理.
            prev_stake_tx = await DstInOutStake.findAll('`pos_time`<=? and `userid`=?', [pos_time, userid],
                                                        orderBy='`pos_time` desc', limit=2)
            prev_start_tx_count = len(prev_stake_tx)
            if prev_start_tx_count == 0:
                prev_stake = Decimal('0')
                prev_start_amount = Decimal('0')
            elif current_tx_userid != userid:
                if prev_stake_tx[0].pos_time == pos_time:
                    # 这次记录已经在之前处理了.
                    processed_sum_stake += Decimal(str(prev_stake_tx[0].stake))
                    processed_sum_pos_profit += Decimal(str(prev_stake_tx[0].pos_profit))
                    continue
                else:
                    prev_stake = Decimal(str(prev_stake_tx[0].stake))
                    prev_start_amount = Decimal(str(prev_stake_tx[0].start_amount))
            else:
                if prev_start_tx_count == 1:
                    prev_stake = Decimal('0')
                    prev_start_amount = Decimal('0')
                else:
                    prev_stake = Decimal(str(prev_stake_tx[1].stake))
                    prev_start_amount = Decimal(str(prev_stake_tx[1].start_amount))

            # 计算用户在这条记录之前的获得的数额
            # with localcontext() as ctx:
            #     ctx.prec = 8
            # 计算用户从上条记录开始的收益
            if user_index == user_count:
                pos_profit = stage_pos_profit - processed_sum_pos_profit
                fix_amount = pos_profit - (stage_pos_profit * prev_stake).__round__(const.PREC_BALANCE)
            else:
                pos_profit = (stage_pos_profit * prev_stake).__round__(const.PREC_BALANCE)
                processed_sum_pos_profit += pos_profit
                fix_amount = 0

            logging.info('[%s]前一条股份记录:股份:%s, 开始数额:%s' % (username, prev_stake, prev_start_amount))
            comment_flag = 'deposit'
            if change_amount < 0:
                comment_flag = 'withdraw'

            if userid == current_tx_userid:
                # 计算用户在这条记录上开始的数额,
                new_start_amount = prev_start_amount + change_amount + pos_profit
                # 计算用户在这条记录上所占的股份比
                comment_template = '{} coin{}'
                if user_index == user_count:
                    new_stake = Decimal('1') - processed_sum_stake
                    fix_stake = new_stake - (new_start_amount / mature_balance).__round__(const.PREC_STAKE)
                    comment = comment_template.format(comment_flag,
                                                      ', fix stake:{}, fix amount:{}'.format(fix_stake, fix_amount))
                else:
                    new_stake = (new_start_amount / mature_balance).__round__(const.PREC_STAKE)
                    processed_sum_stake += new_stake
                    fix_stake = 0
                    comment = comment_flag.format(comment_flag, '')
                logging.info(
                    'c[%s]新股份记录:开始数据:%s, 股份:%s, PoS利息:%s' % (
                        username, new_start_amount, new_stake, pos_profit))
                tx.stake = new_stake
                tx.start_amount = new_start_amount
                tx.pos_profit = pos_profit
                tx.fix_amount = fix_amount
                tx.fix_stake = fix_stake
                tx.start_balance = mature_balance
                tx.stage_pos_profit = stage_pos_profit
                tx.isprocess = 1
                tx.comment = comment
                await tx.update()
                prev_tx = tx
            else:
                # 其他用户的计算
                pos_time_str = tx.pos_time_str
                new_start_amount = prev_start_amount + pos_profit
                comment_template = 'other {} coin{}'
                if user_index == user_count:
                    new_stake = Decimal('1') - processed_sum_stake
                    fix_stake = new_stake - (new_start_amount / mature_balance).__round__(const.PREC_STAKE)
                    comment = comment_template.format(comment_flag,
                                                      ', fix stake:{}, fix amount:{}'.format(fix_stake, fix_amount))
                else:
                    new_stake = (new_start_amount / mature_balance).__round__(const.PREC_STAKE)
                    processed_sum_stake += new_stake
                    fix_stake = 0
                    comment = comment_template.format(comment_flag, '')

                logging.info('o[%s]新股份记录:开始数据:%s, 股份:%s, PoS利息:%s' % (username, new_start_amount,
                                                                      new_stake, pos_profit))
                now_stake_info = DstInOutStake(txid="notxid%s" % next_id(), userid=userid, username=username,
                                               change_amount=pos_profit, stake=new_stake,
                                               start_amount=new_start_amount, pos_profit=pos_profit,
                                               fix_amount=fix_amount, fix_stake=fix_stake,
                                               start_balance=mature_balance, stage_pos_profit=stage_pos_profit,
                                               txtime=pos_time, txtime_str=pos_time_str, pos_time=pos_time,
                                               pos_time_str=pos_time_str, isprocess=1, isonchain=0,
                                               change_username=current_tx_username, comment=comment)
                await now_stake_info.save()

        # if pos_time == 1523256402:
        #     break
        # count = count + 1
        # if count == 4:
        #     break


async def __daily_pos_profit_job():
    """
    pos收益统计, 计算每天的数量, 使用GMT时间作每天的分割
    :return:
    """
    # 本次任务计算结束的总时间:
    # get_info = dstracmd.getinfo()
    # now_time_fix_offset = int(time.time()) + get_info.timeoffset
    block_last_time = dstracmd.getbestblock().time
    # 确定本次计算开始的时间, 这个时间有两种情况, 当天有股份重新分配, 从新股份之后的时间算起(不包括新股份启用时间)
    # 如果没有新股份,从零点开始算起, 包括零点的时间

    last_daily_profit = await DstDailyProfit.findAll(orderBy="profit_time DESC", limit=1)
    if len(last_daily_profit):
        #  如果是2018-4-17 23:59:59
        daily_profit_start_time = last_daily_profit[0].profit_time
    else:
        earliest_stake = await DstInOutStake.findAll(orderBy='pos_time', limit=1)
        if len(earliest_stake):
            daily_profit_start_time = earliest_stake[0].pos_time
        else:
            return

    while True:
        # 开始时间要比上一轮结束时间多一秒 搜索的时候包括这个时间
        # 2018-4-18 00:00:00
        daily_profit_start_time += 1

        # 2018-4-18 23:59:59
        dailyflag = get_timestamp_daily_last_second(daily_profit_start_time)

        # 确定每轮计算的结束时间 (搜索的时候不包括这个时间)
        # 首先获取第二天第一秒的时候,但是处理的时候是不包括第二天第一秒时的收入的
        # 2018-4-18 23:59:59 + 1 秒
        step_end_time = get_timestamp_daily_last_second(daily_profit_start_time) + 1
        # 如果这个时间比本次任务计算结束总时间大的话, 就设为本次任务计算结束的总时间
        if step_end_time > block_last_time:
            step_end_time = block_last_time + 1
        # 再根据 step_end_time 查看从开始时间到结束时间之内有没有股权变更的记录

        dst_in_out_stakes = await DstInOutStake.findAll('`pos_time`<? and `pos_time`>=?',
                                                        [step_end_time, daily_profit_start_time],
                                                        orderBy='pos_time', limit=1)
        # 如果期间有股权变更, 结束时间为股权变更的时间.不包括在搜索内的.
        if len(dst_in_out_stakes):
            step_end_time = dst_in_out_stakes[0].pos_time + 1

        logging.info(
            '######:start_time(包含):{},end_time(不包含):{}'.format(get_gmt_time_yyyymmddhhmmss(daily_profit_start_time),
                                                               get_gmt_time_yyyymmddhhmmss(step_end_time)))

        # 计算当前时间段的总收益
        step_pos_profit = (await DstTransactions.findNumber('sum(`amount`)',
                                                            'txtime>=? and txtime <? and (category=? or category=? or category=?)',
                                                            [daily_profit_start_time, step_end_time,
                                                             const.CATEGORY_GENERATE,
                                                             const.CATEGORY_SENDTOSELF, const.CATEGORY_IMMATURE]) or 0)
        logging.info(
            '######: {} step_pos_profit: {}'.format(get_gmt_time_yyyymmddhhmmss(block_last_time), step_pos_profit))
        step_pos_profit = Decimal(str(step_pos_profit))

        # 获取当前处理时间段最老的未成熟币的tx时间
        # oldest_immature_tx = await DstTransactions.findAll()

        # 取出统计时间前的最近的股份分配的pos_time
        lately_stake = await DstInOutStake.findAll('`pos_time`<?', [daily_profit_start_time],
                                                   orderBy='pos_time desc', limit=1)
        lately_stake_post_time = lately_stake[0].pos_time
        # 计算自上次股份分配到统计时间段时总收益
        stage_pos_profit = (await DstTransactions.findNumber('sum(`amount`)',
                                                             'txtime>=? and txtime <? and (category=? or category=? or category=?)',
                                                             [lately_stake_post_time, step_end_time,
                                                              const.CATEGORY_GENERATE,
                                                              const.CATEGORY_SENDTOSELF, const.CATEGORY_IMMATURE]) or 0)
        stage_pos_profit = Decimal(str(stage_pos_profit))

        # 根据lately_stake_post_time取出需要进行计算的人员
        wait_process_users = await DstInOutStake.findAll('`pos_time`=?', [lately_stake_post_time])
        for user in wait_process_users:
            userid = user.userid

            user_stake = Decimal(str(user.stake))
            # 用户当前时间间隔的收益
            user_step_pos_profit = (step_pos_profit * user_stake).__round__(8)
            # 用户该阶段收益
            user_stage_pos_profit = (stage_pos_profit * user_stake).__round__(8)

            # 用户最后的记录
            user_daily_profit_last_item = await DstDailyProfit.findAll('userid=?', [userid],
                                                                       orderBy='profit_time desc',
                                                                       limit=1)

            user_daily_profit_last_item_len = len(user_daily_profit_last_item)
            if user_daily_profit_last_item_len:
                user_daily_profit_last_item = user_daily_profit_last_item[0]
                # user_all_pos_profit_last = Decimal(str(user_daily_profit_last_item.all_pos_profit))
                if user_daily_profit_last_item.dailyflag == dailyflag:
                    user_daily_profit_last = Decimal(str(user_daily_profit_last_item.daily_profit))
                else:
                    user_daily_profit_last = Decimal(0)
            else:
                # user_all_pos_profit_last = Decimal(0)
                user_daily_profit_last = Decimal(0)

            # 用户当天收益 这块需要改进一下, 不要用加前一天的做法
            user_daily_profit = (user_daily_profit_last + user_step_pos_profit).__round__(8)

            # 用户总收益
            # user_all_pos_profit = (user_all_pos_profit_last + user_step_pos_profit).__round__(8)
            ## 用户除当前之前的每天收益和
            prev_daily_rewards_sum = (await DstDailyProfit.findFields('sum(daily_profit) as daily_profit',
                                                                      'userid=? and isdailynode=? and dailyflag<?',
                                                                      [userid, 1, dailyflag]))[0].daily_profit
            if prev_daily_rewards_sum is None:
                prev_daily_rewards_sum = 0
            user_all_pos_profit = (Decimal(str(prev_daily_rewards_sum)) + user_daily_profit).__round__(8)

            # if len(user_daily_profit_item) == 0:
            if user_daily_profit_last_item_len == 0 or user_daily_profit_last_item.pos_time != user.pos_time or user_daily_profit_last_item.dailyflag != dailyflag:

                # 如果已经存在分配记录,把前一条分配记录的isdailynode设为false
                if user_daily_profit_last_item_len and user_daily_profit_last_item.dailyflag == dailyflag:
                    user_daily_profit_last_item.isdailynode = False
                    await user_daily_profit_last_item.update()

                # 用户注入的资金
                user_injection = await DstInOutStake.findNumber('sum(`change_amount`)',
                                                                'pos_time<=? and userid=? and isonchain=1',
                                                                [user.pos_time, userid])
                # if user_injection < 0:
                #     user_all_pos_profit += Decimal(str(user_injection))
                #     user_injection = 0
                #
                #  daily_profit  all_pos_profilt isdailynode
                user_daily_profit_item = DstDailyProfit(userid=userid, username=user.username,
                                                        daily_profit=user_daily_profit,
                                                        stage_pos_profit=user_stage_pos_profit,
                                                        all_pos_profit=user_all_pos_profit,
                                                        injection=user_injection,
                                                        start_amount=user.start_amount, stake=user.stake,
                                                        pos_time=user.pos_time, isdailynode=True,
                                                        dailyflag=dailyflag,
                                                        dailyflag_str=get_gmt_time_yyyymmddhhmmss(dailyflag),
                                                        profit_time=step_end_time - 1,
                                                        profit_time_str=get_gmt_time_yyyymmddhhmmss(
                                                            step_end_time - 1))
                await user_daily_profit_item.save()
                # print('add', user_daily_profit_item)
                pass
            else:
                # user_daily_profit = (user_daily_profit_last + user_step_pos_profit).__round__(8)
                # user_all_pos_profit = (user_all_pos_profit_last + user_step_pos_profit).__round__(8)
                user_daily_profit_last_item.daily_profit = user_daily_profit
                user_daily_profit_last_item.stage_pos_profit = user_stage_pos_profit
                user_daily_profit_last_item.all_pos_profit = user_all_pos_profit
                user_daily_profit_last_item.isdailynode = True
                user_daily_profit_last_item.profit_time = step_end_time - 1
                user_daily_profit_last_item.profit_time_str = get_gmt_time_yyyymmddhhmmss(step_end_time - 1)
                await user_daily_profit_last_item.update()
                # print('update', user_daily_profit_item)
                pass
            pass
        daily_profit_start_time = step_end_time - 1
        # print(now_time_fix_offset, daily_profit_start_time)
        if block_last_time == daily_profit_start_time:
            break
        # print("#### count", count)
        # count += 1
        # if count == 9:
        #     break


async def __daily_pos_profit_job2():
    pass
