
/// @brief Security Jni
/// @author AutoCode
/// @generate date: 2023-09-17 23:12:07
/// [注：本文件为自动生成，不需要人为编辑，若有修改，请通过配置py脚本来重新生成.]

#include <jni.h>
#include <string>

static const char *SIGN = "HHKWOWRF123GDSFG124323";


/// 网络库 secretID 网络鉴权key
extern "C" JNIEXPORT jstring JNICALL
Java_com_xbw_security_SecurityUtil_get00(JNIEnv *env, jobject) {
    std::string content = "HHKWOWRF123GDSFG124323";
    return env->NewStringUTF(content.c_str());
}


/// 微信能力 key 微信支付key
extern "C" JNIEXPORT jstring JNICALL
Java_com_xbw_security_SecurityUtil_get10(JNIEnv *env, jobject) {
    std::string content = "HHKWOWRF123GDSFG124323";
    return env->NewStringUTF(content.c_str());
}


