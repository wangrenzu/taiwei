<template>

  <el-button type="danger" v-if="home.close" @click="closeSocket">暂停</el-button>
  <el-button type="primary" v-if="home.open" @click="startSocket">开始</el-button>
  <span>老客{{ home.new_user_list2.length }}</span>
  <span>新客{{ home.new_user_list3.length }}</span>
  <el-tag>
    根据成功金额排序,新用户蓝色底20秒
  </el-tag>
  <div class="head">
    <div v-for="user in home.new_user_list2" :key="user.id" class="box1">
      <span v-if="home.vipUser_list.some(item => item.name === user.name)" style="background-color: #1a1a1a">
        {{ user.name }}
      </span>
      <span  v-else-if="user.hasOwnProperty('content')" style="background-color: #e1ba20;">
        {{ user.name }}
      </span>
      <span v-else-if="user.item_time>20" style="background-color: white;color: #1a1a1a">
        {{ user.name }}
      </span>
      <span v-else>
        {{ user.name }}
      </span>

      <span style='font-size: 14px'>
        {{ user.back_rate == 0.00 ? '' : (user.back_rate * 100).toFixed(1) + '%' }}
      </span>
      <span>
        {{ user.sum_score }}
      </span>

      <span v-if=" ((user.transit_num || '0') !== '0' && (user.new_user)) ||
                   ((user.success_num || '0') !== '0'&& (user.new_user))"
            style="font-size: 9px;background-color: #505050;color: white">
        {{ (user.new_user ? user.new_user.slice(0, -1) : '').replace('天', '') }}
      </span>
      <span v-else style="font-size: 9px">
        {{ (user.new_user ? user.new_user.slice(0, -1) : '').replace('天', '') }}
      </span>


      <span>
        {{ (user.success_num || '0') === '0' ? '' : '成' + (user.success_num || '0') }}
        {{ (user.back_num || '0') === '0' ? '' : '/退' + (user.back_num || '0') }}
        <span style="background-color:white;color: #e1ba20;font-size:19px ">
          {{ (user.transit_num || '0') === '0' ? '' : '/回头' + (user.transit_num || '0') }}
        </span>
      </span>


      <span>
            <el-button
                link
                type="primary"
                size="small"
                @click.prevent="showUserInfo(user)"
            >
              详细
            </el-button>
          </span>

    </div>
  </div>
  <div class="bottom">
  <div v-for="user in home.new_user_list3" :key="user.id" class="user-container">
    <div v-if="user.hasOwnProperty('content')">
      <div class="chatbubble">
        <div class="text">
          <p>{{user.content}}</p>
        </div>
      </div>
      <div class="new_user_new2">{{ user.name }}</div>
    </div>
    <div v-else-if="user.item_time>20" class="new_user">{{ user.name }}</div>
    <div v-else class="new_user_new">{{ user.name }}</div>
  </div>
</div>



  <div class="middle">
    <span></span>
    <span>实时弹幕</span>
  </div>
  <div class="barrage">
    <div v-for="(item,index) in home.barrage" :key="index" class="barrage-item">
      <span class="uname" style="color: cornflowerblue">{{ item.name + "：" }}</span>
      <span class="contents">{{ item.content }}</span>
    </div>
  </div>


</template>

<script setup>
import home from "../api/home.js";
import {ElMessage} from "element-plus";


// 获取vip用户列表
const getVipUser = () => {
  home.getVipUser().then(response => {
    home.vipUser_list = response.data.original_data
  }).catch(err => {
    ElMessage.error(err)
  })
}
getVipUser()


// 获取所有的用户信息
const getRoomDate = () => {
  home.roomAll().then(response => {
    home.loading = false;
    home.new_user_list = response.data
    // 将计算结果添加到每行的数据中
  }).catch(err => {
    console.log(err)
  })
}
getRoomDate()

// 打开对应的客户的详细信息
const showUserInfo = (user) => {
  const url = '/UserInfo/' + user.name + '/' + user.success_num + '/' + user.back_num + '/' +
      (user.wait_num + user.transit_num) + '/' + home.search_date;
  window.open(url, '_blank');
}

// 在线观众
let user_list = []
// 屏蔽的用户
let user_not_list = ['S姐助理', '小虎牙啦啦', '舔10个酸奶盖盖', '月亮湾', '爱穿裙子的小熊妹妹', '慢慢莱', '野兔', '小梦啊', '小胖也可以仙女']

// 创建websocket连接
let socket = new WebSocket("ws://192.168.1.101:8002/room/123/");
// 监听websocket传输的数据
socket.onmessage = function (event) {
  home.loading = true;
  // 获取传输的在线观众列表
  user_list = JSON.parse(event.data)[1];
  // 筛选出在线观众中，在客户信息中 和 不在屏蔽的用户中的所有用户
  const user_list_nwe2 = home.new_user_list.filter(item => user_list.includes(item.name) && !user_not_list.includes(item.name));
  if (home.new_user_list2.length === 0) {
    // 第一次获取直接获取所有在线观众
    home.new_user_list2 = user_list_nwe2
  } else {
    // 不是第一次获取则把离开直播间的用户从原列表中删除
    home.new_user_list2 = home.new_user_list2.filter(item => user_list_nwe2.some(user => user.name === item.name));
    user_list_nwe2.forEach(user => {
      // 把新进入符合条件的用户加入到在线观众中
      if (!home.new_user_list2.some(item => item.name === user.name)) {
        home.new_user_list2.push(user);
      }
    });
  }

  // 获取不在客户信息排名中并且不在屏蔽的名单中的直播间观众
  const user_list_nwe = user_list
      .filter(name => !home.new_user_list.some(item => item.name === name) && !user_not_list.includes(name))
      .map(name => {
        return {"name": name};
      })
  if (home.new_user_list3.length === 0) {
    home.new_user_list3 = user_list_nwe
  } else {
     // 不是第一次获取则把离开直播间的用户从原列表中删除
    home.new_user_list3 = home.new_user_list3.filter(item => user_list_nwe.some(user => user.name === item.name));
    user_list_nwe.forEach(user => {
      // 把新进入符合条件的用户加入到在线观众中
      if (!home.new_user_list3.some(item => item.name === user.name)) {
        home.new_user_list3.push(user);
      }
    });
  }
  home.loading = false;
  // 在这里处理接收到的数据
};

// 断开websocket连接
const closeSocket = () => {
  home.close = false
  home.open = true
  socket.close();

}
// 重新连接websocket
const startSocket = () => {
  home.close = true;
  home.open = false;

  // 创建新的WebSocket连接
  socket = new WebSocket("ws://192.168.1.101:8002/room/123/");
  // 功能如上
  socket.onmessage = function (event) {
    home.loading = true;
    user_list = JSON.parse(event.data)[1];
    home.new_user_list2 = home.new_user_list.filter(item => user_list.includes(item.name) && !user_not_list.includes(item.name));
    const user_list_nwe = user_list
        .filter(name => !home.new_user_list.some(item => item.name === name) && !user_not_list.includes(name))
        .map(name => {
          return {"name": name};
        })
    if (home.new_user_list3.length === 0) {
      home.new_user_list3 = user_list_nwe
    } else {
      home.new_user_list3 = home.new_user_list3.filter(item => user_list_nwe.some(user => user.name === item.name));
      user_list_nwe.forEach(user => {
        if (!home.new_user_list3.some(item => item.name === user.name)) {
          home.new_user_list3.push(user);
        }
      });
    }
    home.loading = false;
  };
}

// 给每一个在线观众添加一个计时器，计算观众在直播间的时间
const timer_time = () => {
  setInterval(() => {
    home.new_user_list3.forEach(item => {
      if (!item.hasOwnProperty('item_time')) {
        item.item_time = 0;
      }
      item.item_time++;
    });
  }, 1000);
};
timer_time();

// 给每一个不在客户信息中的在线观众添加一个计时器，计算观众在直播间的时间
const timer_time2 = () => {
  setInterval(() => {
    home.new_user_list2.forEach(item => {
      if (!item.hasOwnProperty('item_time')) {
        item.item_time = 0;
      }
      item.item_time++;
    });
  }, 1000);
};
timer_time2();

// 创建websocket连接获取弹幕信息
let socket2 = new WebSocket("ws://192.168.1.101:8002/barrage/123/");
socket2.onmessage = function (event) {
  // 接收信息中的名字，内容和标签
  if (JSON.parse(event.data).length !== 0) {
    JSON.parse(event.data).forEach(item => {
      const name = item["nick_name"];
      const content = item["content"];
      home.barrage.push({name, content})
    })
  }
  const barrageContainer = document.querySelector('.barrage');
  barrageContainer.scrollTop = barrageContainer.scrollHeight;
  lastBarrage()
}


// 计算最后三条弹幕
const lastBarrage = () => {
  const lastThreeItems = home.barrage.slice(-3);
  home.new_user_list3.forEach(user => {
    delete user.content; // 或者删除属性：
  });

  home.new_user_list2.forEach(user => {
    delete user.content; // 或者删除属性： delete user.content;
  });
  lastThreeItems.forEach(lastItem => {
    home.new_user_list3.forEach(user => {
      if (user.name === lastItem.name) {
        user.content = lastItem.content;
      }
    });
    home.new_user_list2.forEach(user => {
      if (user.name.startsWith(lastItem.name)) {
        user.content = lastItem.content;
      }
    });
  });
}
</script>

<style scoped>
.head {
  display: flex;
  flex-wrap: wrap;
}

.bottom {
  display: flex;
  flex-wrap: wrap;
}

.head div {
  width: 23vw;
  /*height: 1.6vw;*/
  margin-left: 0.4vw;
  margin-top: 0.4vw;
}


.box1 {
  display: flex;
  border: 1px solid black;
  height: 1.5vw;
  line-height: 1.5vw;

}

.box1 span {
  border-left: 1px solid black;
  white-space: nowrap; /* 不换行 */
  overflow: hidden; /* 隐藏超出部分 */
  text-overflow: ellipsis; /* 显示省略号 */
  text-align: center;
}

.box1 span:nth-child(1) {
  background-color: cornflowerblue;
  color: white;
  flex: 6;
  border-left: none;
}

.box1 span:nth-child(2) {
  flex: 2.6;
}

.box1 span:nth-child(3) {
  flex: 3;
}

.box1 span:nth-child(4) {
  flex: 2;
}

.box1 span:nth-child(5) {
  flex: 8;
}

.box1 span:nth-child(6) {
  flex: 2;
}

.new_user {

  height: 2vw;

  text-overflow: ellipsis; /* 显示省略号 */
  border-radius: 10%;
  line-height: 2vw;
  overflow: hidden; /* 隐藏超出部分 */
  white-space: nowrap; /* 不换行 */
  margin-right: 2vw;
  margin-top: 0.5vw;
  text-align: center;
}

.new_user_new {
  height: 2vw;
  background-color: cornflowerblue;
  text-overflow: ellipsis; /* 显示省略号 */
  border-radius: 10%;
  line-height: 2vw;
  overflow: hidden; /* 隐藏超出部分 */
  white-space: nowrap; /* 不换行 */
  margin-right: 2vw;
  margin-top: 0.5vw;
  text-align: center;
}

.new_user_new2 {
  height: 2vw;
  background-color: #e1ba20;
  text-overflow: ellipsis; /* 显示省略号 */
  border-radius: 10%;
  line-height: 2vw;
  overflow: hidden; /* 隐藏超出部分 */
  white-space: nowrap; /* 不换行 */
  margin-right: 2vw;
  margin-top: 0.5vw;
  text-align: center;
}


.middle {
  position: absolute;
  width: 20vw;
  height: 5vh;
  top: 60vh;
  right: 1vw;
  background-color: #20212c;
  border-radius: 10px 10px 0 0;
}

.middle span:nth-child(1) {
  position: absolute;
  display: inline-block;
  width: 0.4vw;
  height: 1.4vw;
  background-color: #ccc728;
  top: 0.9vw;
  left: 0;
}

.middle span:nth-child(2) {
  position: absolute;
  font-size: 1vw;
  top: 0.7vw;
  left: 1.3vw;
  color: #d2e0e4;
}

.barrage {
  position: absolute;
  width: 19vw;
  height: 30vh;
  top: 65vh;
  right: 1vw;
  background-color: #262632;
  border-radius: 0 0 10px 10px;
  overflow-y: scroll;
  overflow-x: hidden;
  padding: 1vw 0 0 1vw;
  margin-bottom: 0.5vw;
}

.barrage {
  /* 其他样式... */
  scrollbar-width: thin; /* 在WebKit浏览器上启用滚动条 */
  scrollbar-color: transparent transparent; /* 设置滚动条的颜色为透明 */
}

.barrage::-webkit-scrollbar {
  width: 6px; /* 滚动条宽度 */
  background-color: transparent; /* 设置滚动条的背景颜色为透明 */
}

.barrage::-webkit-scrollbar-thumb {
  background-color: transparent; /* 设置滚动条的滑块颜色为透明 */
}

.barrage-item {
  margin-bottom: 10px;
  padding: 5px;
  color: #ffffff;
  font-size: 0.8vw;
}

.user-container {
  position: relative;
}

.chatbubble {
  position: absolute;
  width: 6vw;
  background-color: #f0f0f0;
  border-radius: 10px;
  padding: 10px;
  bottom: 100%; /* Adjust this to change the bubble position */
  left: 30%; /* Center the bubble */
  transform: translateX(-50%); /* This is necessary when using left: 50% */
  word-wrap: break-word;
  border: 0.8px solid black;
}

.chatbubble::after {
  content: '';
  position: absolute;
  width: 0;
  height: 0;
  border-left: 10px solid transparent;
  border-right: 10px solid transparent;
  border-top: 10px solid #f0f0f0;
  bottom: -10px;
  left: 80px;

}

.text p {
  margin: 0;
  padding: 0;
  word-wrap: break-word; /* Add this line */
}







</style>