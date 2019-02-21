def updatePannageTask():
    fo = open("/Users/pjhubs/Documents/project/case/PIGPEN-Server/test.txt", "w")
    fo.write("写入成功！")

    # 关闭打开的文件
    fo.close()

    # 查出有虚拟狗的用户 uid
    # 通过 uid 找到猪饲料表记录
    # 叠加对应数据，更新赠送猪饲料字段时间

    # 猪饲料账单
