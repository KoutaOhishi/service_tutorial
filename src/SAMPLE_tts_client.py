#! /usr/bin/env python
#coding:utf-8

#tts = text_to_speech

import rospy
from text_to_speech.srv import TextToSpeech

if __name__ == "__main__":
    rospy.init_node("tts_client")

    while not rospy.is_shutdown():
        rospy.wait_for_service("/speech_word")

        try:
            tts = rospy.ServiceProxy("/speech_word", TextToSpeech)
            input_word = raw_input("Input sentence you want to speek. --> ")
            flag = tts(input_word)
            rospy.loginfo(flag)

        except rospy.ServiceException, e:
            rospy.logerr("Service call failed: %s"%e)
