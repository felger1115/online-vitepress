<template>
  <q-page class="q-mx-lg">
    <div class="row-center q-my-lg q-mx-lg justify-between">
      <span>{{$r.currentRoute.value.params.name}}</span>
      <q-btn color="primary" label="编辑" @click="to()" />
      <q-btn color="red-13" label="删除" @click="deleteDoc()" />
    </div>
    <q-markdown :src="content.content"></q-markdown>

    <q-dialog v-model="alert">
      <q-card>
        <q-card-section>
          <div class="text-h6">请注意!</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          删除后将无法找回, 确定删除吗?
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="确定" color="red-4" @click="deleteConfirm" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, watchEffect, inject } from 'vue';
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router';

const $r = useRouter()
const $q = useQuasar()

const authid = inject('authid')


const alert = ref(false)
const content = ref('')

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
    content.value = await resp.json()
  } catch (error) {
    $q.notify('获取失败! ' + error)
  }
}

watchEffect(() => {
  getDoc()
})

const deleteDoc = () => {
  alert.value = true
}
const deleteConfirm = async () => {
  $q.loading.show()
  try {
    let path = `/api/v1/docs/${$r.currentRoute.value.params.name}`
    if ($r.currentRoute.value.query.private) path+='?private=true'
    const resp = await fetch(path, {
      method: 'DELETE',
      headers: {
        'x-authid': authid.value,
        'Content-Type': 'application/json'
      }
    })

    if (!resp.ok) {
      const errorData = await resp.json()
      throw new Error(`API错误: ${resp.status} - ${errorData.message}`)
    }
    content.value = ''
    alert.value = false
    $q.loading.hide()
  } catch (error) {
    $q.loading.hide()
    $q.notify('获取失败! ' + error)
  }
}
function to() {
  if($r.currentRoute.value.query.private) {
    $r.push({path: `/editor/${$r.currentRoute.value.params.name}`, query: {private:  true}})
    return
  }
  $r.push(`/editor/${$r.currentRoute.value.params.name}`)
}
</script>
