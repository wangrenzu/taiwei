<template>
  <div class="center-container">
    <div>
      <span>款号:{{ code }}</span>
      <span> 商品序号:{{ id }}</span>
      <span> 已下单:{{ number }}</span>
    </div>
  </div>

  <div style="display: flex; justify-content: center; align-items: center;margin-top: 5px">
    <el-button type="primary" @click="showUser('买过')">买过</el-button>
    <el-button type="primary" @click="showUser('没买过')">没买过</el-button>
    <el-button type="primary" @click="showUser('全部')">全部</el-button>
  </div>

  <div class="right">
				   <span
               v-for="(item, index) in live_user_info_list"
               :key="item.name + '_' + index"
               class='user_item'
               :class="{'vip_user': hasVipTag(item.tag), 'empty': item.name === ''}"
           >
						<span class='uname' :class="{'timeStyle':item.timer < 15}">{{ item.name }}</span>
                        <span class='contents'>{{ item.content }}</span>
						<span v-if="item.info" class="Purchase_rate">
                  {{ (item.info.success_num || '0') === '0' ? '' : '成' + (item.info.success_num || '0') }}
                  {{ (item.info.back_num || '0') === '0' ? '' : '/退' + (item.info.back_num || '0') }}
                  {{ (item.info.transit_num || '0') === '0' ? '' : '/回' + (item.info.transit_num || '0') }}
						</span>
						<span v-for="tag in item.tag">
							<span :class="tag.cls" v-if='item.name !== ""'>{{ tag.name }}</span>
						</span>
						<span class='timer' v-if='item.name !== ""'>{{ item.timer }}</span>
				  </span>
  </div>

</template>

<script setup>

import {ref, watch} from "vue";
import home from "../api/home.js";
import roomphone from "../api/roomphone.js";
import room from "../api/room.js";

const hasVipTag = (tagArray) => {
  return tagArray.some(tag => tag.name === 'VIP');
}

const b_socket = new WebSocket("ws://192.168.1.137:8000/ws/barrage/S姐直播间");
b_socket.onmessage = (event) => {
  const item = JSON.parse(event.data).content
  const name = item["nick_name"];
  const content = item["content"];
  if (room.not_name.includes(name) || room.not_content.includes(content)) {
    // 在黑名单中，不执行任何操作
    return;
  }
  let item_user = {
    name: name,
    content: content
  }
  roomphone.barrage.push(item_user);
  roomphone.barrage.forEach(barrage => {
    let user = live_user_info_list.value.find(userCopy => userCopy.name === barrage.name);
    if (user) {
      user.content = barrage.content;
    }
  });
}

const getAllUser = () => {
  return new Promise((resolve, reject) => {
    home.roomAll().then(response => {
      roomphone.all_user_list = response.data;
      response.data.forEach(item => {
        roomphone.new_user_list.push(item.name);
        if (((item.transit_num || '0') !== '0' && (item.new_user)) || ((item.success_num || '0') !== '0' && (item.new_user))) {
          roomphone.new_user_list2.push(item.name);
        }
      });
      resolve();  // Promise被解析了
    }).catch(err => {
      console.log(err)
      reject(err);  // Promise被拒绝了
    })
  });
}
getAllUser().then(() => {
  // 这里的代码会在getAllUser执行完之后运行
}).catch(error => {
  console.log(error)
  // 如果在getAllUser中发生错误，这里的代码会被执行
});


const getVip = () => {
  home.getVipUser().then(rep => {
    rep.data.original_data.forEach(item => {
      roomphone.vip_user_list.push(item.name)
    })
  }).catch(err => {
    console.log(err);
  })
}
getVip()


const live_user_list = ref([])
const live_user_info_list = ref([])
const all_live_user_info_list = ref([])

const code = ref('')    //款号
const id = ref('')      //商品序号
const number = ref('')    //已下单


const douyin_user_info = ref([])
const get_live_douyin_user = () => {
  roomphone.addLiveDouyinUser().then(response => {
    let douyin_user_list = response.data.message.ranks
    const nickname_list = []
    douyin_user_list.forEach(item => {
      const nickname = item.user.nickname
      const display_id = item.user.display_id
      const user_fans_club_status = item.user.fans_club.data.user_fans_club_status
      nickname_list.push(nickname)
      //判断用户是否已经存在
      const user = douyin_user_info.value.find(u => u.username === nickname);
      if (!user) {
        const newUser = {
          douyin_id: display_id, // 这里你可能想要生成一个新的ID
          is_fan_group: user_fans_club_status,
          style_number: code.value,
          time: 1,
          username: nickname,
        };
        douyin_user_info.value.push(newUser);
        timer.value[nickname] = setInterval(() => {
          newUser.time++;
        }, 1000);
      } else if (!timer.value[nickname]) {
        // 如果用户已在 douyin_user_info 中，但他们的定时器已停止，则重新启动定时器
        timer.value[nickname] = setInterval(() => {
          user.time++;
        }, 1000);
      }
    })
    // 如果 douyin_user_info 中的用户不在 live_user_list 中，停止他们的定时器
    douyin_user_info.value.forEach(user => {
      if (!nickname_list.includes(user.username) && timer.value[user.username]) {
        clearInterval(timer.value[user.username]);
        delete timer.value[user.username];
      }
    });


    if (live_user_list.value === nickname_list) {
      return
    }
    const incomingUsers = nickname_list;

    live_user_list.value = incomingUsers;

    incomingUsers.forEach(item => {
      let existingUser = live_user_info_list.value.find(userCopy => userCopy.name === item);
      if (!existingUser) {
        let tag = [];
        let info = {};
        if (roomphone.vip_user_list.includes(item)) {
          tag.push({name: 'VIP', cls: "VIP"});
        }
        if (!roomphone.new_user_list.includes(item)) {
          tag.push({name: '新客', cls: "newUser2"});
        }
        if (roomphone.new_user_list2.includes(item)) {
          tag.push({name: '新客回头', cls: "newUser"});
        }
        info = roomphone.all_user_list.find(user => user.name === item);

        const intervalId = setInterval(() => {
          const userToUpdate = live_user_info_list.value.find(user => user.name === item);
          if (userToUpdate) {
            userToUpdate.timer++;
          }
        }, 1000);

        live_user_info_list.value.push({
          name: item,
          timer: 1,
          tag: tag,
          info: info,
          content: '',
          intervalId: intervalId  // Add the interval ID here
        });
      }
    });
    // Check for users that have left the room and remove them from live_user_info_list
    const usersToRemove = live_user_info_list.value.filter(user => !incomingUsers.includes(user.name));
    usersToRemove.forEach(user => {
      const index = live_user_info_list.value.findIndex(userCopy => userCopy.name === user.name);
      if (index !== -1) {
        clearInterval(user.intervalId);  // Clear the timer for the user who left
        live_user_info_list.value.splice(index, 1);
      }
    });
    all_live_user_info_list.value = live_user_info_list.value
  }).catch(err => {
    console.log(err);
  })
}


const addUser = () => {
  roomphone.addUser(douyin_user_info.value).then(response => {
  }).catch(err => {
    console.log(err)
  })
}
const timer = ref({})
const clearAllTimers = () => {
  for (let key in timer.value) {
    clearInterval(timer.value[key]);
  }
}
const getCode = () => {
  room.get_code().then(response => {
    if (response.data.data.code !== code.value || response.data.data.number !== number.value) {
      addUser()
      clearAllTimers()
      timer.value = {}
      douyin_user_info.value = []
      code.value = response.data.data.code
      id.value = response.data.data.id
      number.value = response.data.data.number
    }
  }).catch(err => {
    console.log(err)
  })
}
getCode()


// 当页面关闭的时候，清除定时器
window.onbeforeunload = function () {
  clearInterval(intervalId2);
  clearInterval(intervalId3);
};


// 每5秒执行一次
let intervalId2 = setInterval(getCode, 5000);
//每一秒
let intervalId3 = setInterval(get_live_douyin_user, 2000)

const buy_code_user_list = ref([])
const showUser = (type) => {
  clearInterval(intervalId3);
  if (type === "没买过") {
    live_user_info_list.value = all_live_user_info_list.value
        .filter(user => !buy_code_user_list.value.includes(user.name))
  } else if (type === "买过") {
    live_user_info_list.value = all_live_user_info_list.value
        .filter(user => buy_code_user_list.value.includes(user.name))
  } else {
    live_user_info_list.value = all_live_user_info_list.value
    intervalId3 = setInterval(get_live_douyin_user, 1000);
  }
}


//直播间的商品有多少人买过

const getUser = () => {
  roomphone.getUser(code.value).then(response => {
    buy_code_user_list.value = response.data.data
  }).catch(err => {
    console.log(err)
  })
}
getUser()

watch(
    () => code.value,
    () => {
      getUser()
    }
)

</script>

<style scoped>

.center-container {
  height: 100%;
  display: grid;
  place-items: center;
}

.left div {
  flex: 1;
  width: 35%;
  height: 10vh;
  line-height: 5vh;
  background-color: #502c75;
  margin-top: 10vh;
  margin-bottom: 10vh;
  font-size: 1vw;
  margin-left: 0.6vw;
  border-radius: 5px;
  text-align: center;
}

.left div a {
  display: inline-block;
  width: 100%;
  height: 100%;
  color: white;
  text-decoration: none;
  text-align: center;
}

/* 这是给用户名设置的样式 */
.user_item {
  position: relative;
  display: inline-block;
  width: 30vw;
  height: 10vh;
  background-color: #502C75;
  margin-left: 1vw;
  margin-top: 1vw;
  border-radius: 10px;
}

.user_item .uname {
  position: absolute;
  left: 0.5vw;
  top: 0;
  font-size: 0.8vw;
  color: #7bbde0;
}

.user_item .timer {
  position: absolute;
  font-size: 3.5vw;
  color: rgba(255, 255, 255, 0.42);
  bottom: 0;
  right: 0;
}

/* 这是隐藏的发消息的框的样式 */
.message {
  position: relative;
  position: absolute;
  top: 20vw;
  left: 40vw;
  width: 20vw;
  height: 30vh;
  background-color: #2e4585;
  border-radius: 10px;
  opacity: 0.8;
}


button {
  cursor: pointer;
}

.vip_user {
  border: 1px solid #171212;
}

.Purchase_rate {
  position: absolute;
  bottom: 0;
  display: inline-block;
  width: 80%;
  height: 2vh;
  background-color: #2e4585;
  color: rgba(255, 255, 255, 0.69);
  border-radius: 10px;
  text-align: center;
  line-height: 2vh;
  font-size: 7px;
}

.tag_name {
  color: darkred;
}


.contents {
  position: absolute;
  top: 8vw;
  display: inline-block;
  width: 100%;
  height: 3vh;
  border-radius: 10px;
  color: white;
  font-size: 10px;
}

.right .empty {
  background-color: rgb(80, 44, 117, 0.2);
}

.user_item .timeStyle {
  color: red;
}


.r_content div {
  border-radius: 20px;
  margin-right: 1.5vw;
}

.r_content div:nth-child(1) {
  display: flex;
  flex: 1.67;
  flex-direction: column;
}


.r_top input {
  width: 90%;
  height: 20%;
  border: 2px solid #423f86;
  border-radius: 10px;
  text-align: center;
  margin-left: 1vw;
  margin-top: 2vw;
  font-size: 1vw;
}

.r_top button {
  width: 7vw;
  height: 4vh;
  border-radius: 10px;
  text-align: center;
  margin-left: 8vw;
  margin-top: 1vw;
  font-size: 1vw;
  border: 1px solid rgba(255, 255, 255, 0.58);
  color: rgba(255, 255, 255, 0.42);
  background-color: rgba(255, 255, 255, 0.42);
  cursor: pointer; /* 鼠标放上去显示小手 */
}

.r_top button:hover {
  background-color: rgba(255, 255, 255, 0.24);
}


/*中间部分的样式*/
.r_content div:nth-child(2) {
  overflow: hidden;
  flex: 2;
  display: flex;
  flex-direction: column;
  background-color: rgba(49, 55, 99, 0.7);
}

.newUser {
  position: absolute;
  top: 4vw;
  display: inline-block;
  width: 15vw;
  height: 2vh;
  border-radius: 10px;
  background-color: pink;
  color: black;
  text-align: center;
  opacity: 0.7;
  font-size: 5px;
}

.newUser2 {
  position: absolute;
  bottom: 0;
  left: 1vw;
  color: #00ff00;
  font-size: 1.2vw;
}

.VIP {
  position: absolute;
  top: 0;
  right: 0;
  display: inline-block;
  width: 8vw;
  font-size: 14px;
  height: 2vh;
  border-radius: 10px;
  background-color: #2c0b0e;
  color: white;
  text-align: center;
  line-height: 2vh;
  opacity: 0.8;
}

</style>