<template>
  <div class="product-list-page"> 
    <div>
      <h1>当前价格</h1>
    <div class="table-container">
    <table class="product-list">
      <!-- 表格1内容：显示前10条数据 -->
      <thead>
        <tr>
          <th>名称</th>
          <th>标志</th>
          <th>价格</th>

        </tr>
      </thead>
      <tbody>
        <tr v-for="obj in prices" :key="obj.id">
          <td>
            <div>{{ obj.name }}</div>
          </td>
          <td>
            <div>{{ obj.symbol }}</div>
          </td>
          <td>
            <div>{{ obj.latest_price}}</div>
          </td>

        </tr>
      </tbody>
    </table>
  </div>
    </div>
  </div>

  </template>
  
  <script>
  import { GETprice} from "@/request/api.js"

  export default {
    data() {
      return {
        prices: [],
      }
    },
  mounted() {

       GETprice().then(response => {
      this.prices = response
    }).catch(error => {
      console.error('完整错误信息:', error);
      // 错误信息增强
      alert(`请求失败: ${error.message || '网络异常'}\n请检查：
  1. 网络连接
  2. 接口地址是否正确
  3. 控制台完整错误日志`);
    });}

  }
  </script>
 
<style scoped>
.product-list-page {
  padding: 20px;
  background: linear-gradient(to right, #6dd5ed, #2193b0); /* 添加酷炫的背景渐变 */
}

h1 {
  text-align: center;
  color: #333;
}

button {
  background-color: #007bff;
  color: white;
  padding: 2px 5px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin: 0 5px;
}
</style>

