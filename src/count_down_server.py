#! /usr/bin/env python
#coding:utf-8
import rospy
from service_tutorial.srv import CountDown

def server(srv):
    count = srv.second

    while count != 0:
        rospy.loginfo(count)
        count -= 1
        rospy.sleep(1)

    rospy.loginfo("Finish")
    return True


if __name__ == "__main__":
    rospy.init_node("count_down_server") #ノードの宣言

    rospy.loginfo(" count_down_server ON ")

    #rospy.Service(サービス名, サービスの型, 呼ばれたら実行する関数)
    rospy.Service("/count_down", CountDown, server)

    rospy.spin()
