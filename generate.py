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


