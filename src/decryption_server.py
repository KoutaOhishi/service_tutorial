#! /usr/bin/env python
#coding:utf-8
"""
サーバ：暗号解読をする側
"""
import rospy
from service_tutorial.srv import Decryption

def decoder(srv):
    import codecs
    return codecs.decode(str(srv.input), "rot13")

if __name__ == "__main__":
    rospy.init_node("decription_server") #ノードの宣言
    rospy.loginfo(" description_server ON ")
    #rospy.Service(サービス名, サービスの型, 呼ばれたら実行する関数)
    rospy.Service("/decription", Decryption, decoder)

    rospy.spin()
