import axios from "axios";

// 常量定义
const REQUEST_TIMEOUT = 30000;
const CONTENT_TYPE = "application/json;charset=UTF-8";
const TOKEN_KEY = "token";

// HTTP 状态码常量
const HTTP_STATUS = {
  SUCCESS: 200,
  CREATED: 201,
  UNAUTHORIZED: 401,
  INTERNAL_SERVER_ERROR: 500,
};

// 错误消息常量
const ERROR_MESSAGES = {
  TOKEN_EXPIRED: "登录已过期，请重新登录！",
  AUTHENTICATION_FAILED: "签名验证失败",
};

// 创建axios实例
const request = axios.create({
  headers: {
    "Content-Type": CONTENT_TYPE,
  },
  timeout: REQUEST_TIMEOUT, // 修正拼写错误
});

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (token) {
      config.headers.Authorization = token;
    }
    return config;
  },
  (error) => {
    console.error("请求错误:", error);
    return Promise.reject(error);
  }
);

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    const { status, data } = response;
    
    // 处理成功响应
    if (status === HTTP_STATUS.SUCCESS || status === HTTP_STATUS.CREATED) {
      return data.code === 0 ? data : Promise.resolve(data);
    }
    
    // 其他成功状态码处理
    return Promise.resolve(data);
  },
  (error) => {
    const { response } = error;
    
    if (!response) {
      console.error("网络错误:", error);
      return Promise.reject(error);
    }

    const { status, data } = response;

    // 处理 token 过期或认证失败
    if (status === HTTP_STATUS.INTERNAL_SERVER_ERROR && 
        data.msg?.includes(ERROR_MESSAGES.AUTHENTICATION_FAILED)) {
      handleTokenExpired();
    } else if (status === HTTP_STATUS.UNAUTHORIZED) {
      // 处理 401 未授权
      handleTokenExpired();
    }

    // 统一错误消息处理
    const errorMessage = data?.msg || `请求失败，状态码: ${status}`;
    console.error("响应错误:", errorMessage);
    
    return Promise.reject(errorMessage);
  }
);

// Token 过期处理函数
const handleTokenExpired = () => {
  alert(ERROR_MESSAGES.TOKEN_EXPIRED);
  
  setTimeout(() => {
    localStorage.removeItem(TOKEN_KEY);
    // 使用 window.location.href 确保完全重定向
    window.location.href = "/login";
  }, 50000);
};

export default request;