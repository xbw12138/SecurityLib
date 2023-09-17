# SecurityLib
Android Key Security Encryption Native Auto Generation so

## Description
Write the key information into the security.json file in the root directory, execute the generate.py script in the root directory, and automatically generate JNI information, which can be packaged into a jar file. At the same time, the key information will be injected into the so file。

`python generate.py`

`./gradlew assembleDebug`

security.json
```Json
{
  "signature": "HHKWOWRF123GDSFG124323",
  "security" : [
    {
      "name": "网络库",
      "data": [
        {
          "name": "secretID",
          "value": "HHKWOWRF123GDSFG124323",
          "describe": "网络鉴权key"
        }
      ]
    },
    {
      "name": "微信能力",
      "data": [
        {
          "name": "key",
          "value": "HHKWOWRF123GDSFG124323",
          "describe": "微信支付key"
        }
      ]
    }
  ]
}
```

generate.py
```Python
import os, sys, re, json
from datetime import datetime

# 获取当前文件所在的目录
current_directory = os.path.dirname(__file__)

# 构建相对路径
security_file_path = os.path.join(current_directory, "security.json")
cpp_file_path = os.path.join(current_directory, "app", "src", "main", "cpp", "info.cpp")
java_file_path = os.path.join(current_directory, "app", "src", "main", "java", "com", "xbw", "securitylib", "SecurityUtil.java")

cpp_code = """
/// @brief Security Jni
/// @author AutoCode
/// @generate date: ${GENE_DATE}
/// [注：本文件为自动生成，不需要人为编辑，若有修改，请通过配置py脚本来重新生成.]

#include <jni.h>
#include <string>

static const char *SIGN = "${SIGNATURE}";

${SECURITY_JNI_LIST}
"""

cpp_code_jni = """
/// ${SECURITY_DESCRIBE}
extern "C" JNIEXPORT jstring JNICALL
Java_com_xbw_securitylib_SecurityUtil_${FUNCTION_NAME}(JNIEnv *env, jobject) {
    std::string content = "${SECURITY_VALUE}";
    return env->NewStringUTF(content.c_str());
}

"""

java_code = """
package com.xbw.securitylib;

/// @brief Security Jni
/// @author AutoCode
/// @generate date: ${GENE_DATE}
/// [注：本文件为自动生成，不需要人为编辑，若有修改，请通过配置py脚本来重新生成.]

public class SecurityUtil {

  static {
    System.loadLibrary("securitylib");
  }

  ${FUNCTION_NAME_LIST}
}

"""

java_code_function = """
  /**
   * ${SECURITY_DESCRIBE}
   * @return ${RETURN_VALUE}
   */
  public static native String ${FUNCTION_NAME}();
"""

with open(security_file_path) as file:
    data = json.load(file)
    cpp_code_content = ""
    java_code_content = ""
    security = data["security"]
    signature = data["signature"]
    for i in range(len(security)):
        type_name = security[i]["name"];
        type_data = security[i]["data"];
        for j in range(len(type_data)):
            security_name = type_data[j]["name"];
            security_value= type_data[j]["value"];
            security_describe = type_data[j]["describe"];
            function_name = "get" + str(i) + str(j);
            tmp_cpp_code_jni = cpp_code_jni.replace("${SECURITY_DESCRIBE}", type_name + " " + security_name + " " + security_describe) \
                .replace("${FUNCTION_NAME}", function_name) \
                .replace("${SECURITY_VALUE}", security_value)
            tmp_java_code_function = java_code_function.replace("${SECURITY_DESCRIBE}", type_name + " " + security_name) \
                .replace("${RETURN_VALUE}", security_describe) \
                .replace("${FUNCTION_NAME}", function_name)
            cpp_code_content += tmp_cpp_code_jni
            java_code_content += tmp_java_code_function

    formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpp_code = cpp_code.replace("${SECURITY_JNI_LIST}", cpp_code_content) \
        .replace("${GENE_DATE}", formatted_time) \
        .replace("${SIGNATURE}", signature);
    java_code = java_code.replace("${FUNCTION_NAME_LIST}", java_code_content) \
        .replace("${GENE_DATE}", formatted_time);

    with open(cpp_file_path, "w") as file:
        file.write(cpp_code)
    with open(java_file_path, "w") as file:
        file.write(java_code)
```

Verify Android signature information in so file

security.cpp
```cpp
#include <jni.h>
#include <string>
#include "info.cpp"


static int verifySign(JNIEnv *env);

jint JNI_OnLoad(JavaVM *vm, void *reserved) {
    JNIEnv *env = NULL;
    if (vm->GetEnv((void **) &env, JNI_VERSION_1_4) != JNI_OK) {
        return JNI_ERR;
    }
    if (verifySign(env) == JNI_OK) {
        return JNI_VERSION_1_4;
    }
    // 签名不一致!
    return JNI_ERR;
}

static jobject getApplication(JNIEnv *env) {
    jobject application = NULL;
    jclass activity_thread_clz = env->FindClass("android/app/ActivityThread");
    if (activity_thread_clz != NULL) {
        jmethodID currentApplication = env->GetStaticMethodID(
                activity_thread_clz, "currentApplication", "()Landroid/app/Application;");
        if (currentApplication != NULL) {
            application = env->CallStaticObjectMethod(activity_thread_clz, currentApplication);
        } else {
            // Cannot find method: currentApplication() in ActivityThread.
        }
        env->DeleteLocalRef(activity_thread_clz);
    } else {
        // Cannot find class: android.app.ActivityThread
    }

    return application;
}



static int verifySign(JNIEnv *env) {
    // Application object
    jobject application = getApplication(env);
    if (application == NULL) {
        return JNI_ERR;
    }
    // Context(ContextWrapper) class
    jclass context_clz = env->GetObjectClass(application);
    // getPackageManager()
    jmethodID getPackageManager = env->GetMethodID(context_clz, "getPackageManager",
                                                   "()Landroid/content/pm/PackageManager;");
    // android.content.pm.PackageManager object
    jobject package_manager = env->CallObjectMethod(application, getPackageManager);
    // PackageManager class
    jclass package_manager_clz = env->GetObjectClass(package_manager);
    // getPackageInfo()
    jmethodID getPackageInfo = env->GetMethodID(package_manager_clz, "getPackageInfo",
                                                "(Ljava/lang/String;I)Landroid/content/pm/PackageInfo;");
    // context.getPackageName()
    jmethodID getPackageName = env->GetMethodID(context_clz, "getPackageName",
                                                "()Ljava/lang/String;");
    // call getPackageName() and cast from jobject to jstring
    jstring package_name = (jstring) (env->CallObjectMethod(application, getPackageName));
    // PackageInfo object
    jobject package_info = env->CallObjectMethod(package_manager, getPackageInfo, package_name, 64);
    // class PackageInfo
    jclass package_info_clz = env->GetObjectClass(package_info);
    // field signatures
    jfieldID signatures_field = env->GetFieldID(package_info_clz, "signatures",
                                                "[Landroid/content/pm/Signature;");
    jobject signatures = env->GetObjectField(package_info, signatures_field);
    jobjectArray signatures_array = (jobjectArray) signatures;
    jobject signature0 = env->GetObjectArrayElement(signatures_array, 0);
    jclass signature_clz = env->GetObjectClass(signature0);

    jmethodID toCharsString = env->GetMethodID(signature_clz, "toCharsString",
                                               "()Ljava/lang/String;");
    // call toCharsString()
    jstring signature_str = (jstring) (env->CallObjectMethod(signature0, toCharsString));

    // release
    env->DeleteLocalRef(application);
    env->DeleteLocalRef(context_clz);
    env->DeleteLocalRef(package_manager);
    env->DeleteLocalRef(package_manager_clz);
    env->DeleteLocalRef(package_name);
    env->DeleteLocalRef(package_info);
    env->DeleteLocalRef(package_info_clz);
    env->DeleteLocalRef(signatures);
    env->DeleteLocalRef(signature0);
    env->DeleteLocalRef(signature_clz);

    const char *sign = env->GetStringUTFChars(signature_str, NULL);
    if (sign == NULL) {
        // 分配内存失败
        return JNI_ERR;
    }

    int result = strcmp(sign, SIGN);
    // 使用之后要释放这段内存
    env->ReleaseStringUTFChars(signature_str, sign);
    env->DeleteLocalRef(signature_str);
    if (result == 0) { // 签名一致
        return JNI_OK;
    }

    return JNI_ERR;
}
```