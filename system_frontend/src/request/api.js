//引入request.js文件
import request from "./request.js";

const BaseUrl = "http://8.218.4.242:8888/dashboard/api/";
// const BaseUrl = "http://localhost:8888/dashboard/api/";
// const previewTextUrl = process.env.VUE_APP_BASE_API_previewText



export function GETprice() {
  return request({
    baseURL: BaseUrl,
    url: "/lastest_price/",
    method: "GET",
  });
}
