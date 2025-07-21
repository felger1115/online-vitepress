<template>
  <q-page class="q-mx-lg">
    <div class="row-center q-my-lg q-mx-lg justify-between">
      <q-input v-model="title" type="text" label="名称,全小写,影响url地址" />
      <div>
        <span>私有:</span>
        <q-toggle v-model="is_private" color="green" />
      </div>
      <q-btn color="yellow-10" label="返回" @click="()=>$r.back()" />
      <q-btn color="primary" :loading="saveLoading" label="保存" @click="saveDoc" />
    </div>
    <MdEditor v-model="content" :theme="theme"/>
  </q-page>
</template>

<script setup>
import { ref, computed, markRaw, watch, onMounted, inject } from 'vue';
import { useQuasar } from 'quasar'
import { MdEditor } from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
import { useRouter } from 'vue-router';

const $r = useRouter()
const $q = useQuasar()

const theme = computed(() => {
  return $q.dark.isActive ? 'dark' : 'light'
})
const isNew = computed(() => {
  return $r.currentRoute.value.params.name === '_'
})

const authid = inject('authid')


// 获取当前日期，格式为YYYY-MM-DD
// const getCurrentDate = () => {
//   const now = new Date()
//   const year = now.getFullYear()
//   const month = String(now.getMonth() + 1).padStart(2, '0')
//   const day = String(now.getDate()).padStart(2, '0')
//   return `${year}-${month}-${day}`
// }

// 文章模板
// const defaultTemplate = ''
// const defaultTemplate = `---
// post: true
// title: 文章标题
// date: ${getCurrentDate()}
// cover: 图片连接
// coveross: 备用连接
// categories:
//  - 分类
// tags:
//  - 标签
// description: 在此处添加文章描述，会显示在文章列表中。
// ---
// 文章内容
// `;
// const content = shallowRef(defaultTemplate);
const content = ref('');
const title = ref('')
const is_private = ref(true)
const saveLoading = ref(false)

const saveDoc = async () => {
  if (!title.value) {
    $q.notify('请输入文章名称')
    return
  }

  saveLoading.value = true
  const fileContent = typeof content.value === 'string' ? content.value : JSON.stringify(markRaw(content.value))

  try {

    // 准备请求体
    const requestBody = {
      content: fileContent,
      name: title.value
    }

    if (is_private.value) {
      requestBody.private = true
    }

    const resp = await fetch(`/api/v1/docs`, {
      method: 'POST',
      headers: {
        'x-authid': authid.value,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    })

    if (!resp.ok) {
      const errorData = await resp.json()
      throw new Error(`保存API错误: ${resp.status} - ${errorData.message}`)
    }
    $q.notify('保存成功!')
  } catch (error) {
    $q.notify('保存失败! ' + error)
  } finally {
    saveLoading.value = false
  }
}

const getDoc = async () => {
  if (!$r.currentRoute.value.params.name) {
    return
  }
  try {
    let path = `/api/v1/docs/${$r.currentRoute.value.params.name}`
    if ($r.currentRoute.value.query.private) path+='?private=true'
    const resp = await fetch(path, {
      method: 'GET',
      headers: {
        'x-authid': authid.value,
        'Content-Type': 'application/json'
      }
    })

    if (!resp.ok) {
      const errorData = await resp.json()
      throw new Error(`API错误: ${resp.status} - ${errorData.message}`)
    }
    const data = await resp.json()
    content.value = data.content
  } catch (error) {
    $q.notify('获取失败! ' + error)
  }
}

watch(() => $r.currentRoute.value.params.name, (newV) => {
  if (newV === '_') {
    content.value = ''
    title.value = ''
    is_private.value = false
  }
})

function init() {
  title.value = $r.currentRoute.value.params.name
  is_private.value = !!$r.currentRoute.value.query.private
  getDoc()
}
onMounted(() => {
  if (!isNew.value) {
    init()
  }
})
</script>
