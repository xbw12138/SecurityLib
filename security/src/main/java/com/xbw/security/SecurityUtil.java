
package com.xbw.security;

/// @brief Security Jni
/// @author AutoCode
/// @generate date: 2023-09-17 23:12:07
/// [注：本文件为自动生成，不需要人为编辑，若有修改，请通过配置py脚本来重新生成.]

public class SecurityUtil {

  static {
    System.loadLibrary("security");
  }

  
  /**
   * 网络库 secretID
   * @return 网络鉴权key
   */
  public static native String get00();

  /**
   * 微信能力 key
   * @return 微信支付key
   */
  public static native String get10();

}

