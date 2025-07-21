<template>
  <q-layout view="HHh lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn flat dense round icon="mdi-menu" aria-label="Menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          WUK Press
        </q-toolbar-title>

        <div>

          <q-btn outline icon="mdi-refresh" label="刷新列表" @click="getDocsList()" />
          <q-btn class="q-mx-lg" outline icon="mdi-note-edit-outline" label="新建" @click="toCreate()" />
        </div>
        <div>
          <q-btn class="q-mx-lg bg-green" outline icon="mdi-cube-send" label="发布" @click="onPush()" />

        </div>
        <q-btn flat dense round icon="mdi-theme-light-dark" @click="() => $q.dark.toggle()" />
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-tabs v-model="tab" class="text-teal">
        <q-tab name="public" label="公开" />
        <q-tab name="private" label="私有" />
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="public">
          <EssentialLink v-for="link in publicLinksList" :key="link.title" v-bind="link" />
        </q-tab-panel>
        <q-tab-panel name="private">
          <EssentialLink v-for="link in privateLinksList" :key="link.title" v-bind="link" />
        </q-tab-panel>
      </q-tab-panels>

    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, inject } from 'vue'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import EssentialLink from 'components/EssentialLink.vue'

const $q = useQuasar()
const $r = useRouter()

const authid = inject('authid')
const build = inject('build')

const leftDrawerOpen = ref(false)
const tab = ref('public')

const publicLinksList = ref([
  {
    title: 'Home',
    link: '#/'
  },
])
const privateLinksList = ref([
  {
    title: 'Home',
    link: '#/'
  },
])

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
function toCreate() {
  $r.push({path:'/editor/_'})
}

const getDocsList = async () => {
  try {
    const resp = await fetch(`/api/v1/docs-list?includes=private`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'x-authid': authid.value
      }
    })

    if (!resp.ok) {
      const errorData = await resp.json()
      throw new Error(`API错误: ${resp.status} - ${errorData.message}`)
    }
    const data = await resp.json()
    publicLinksList.value = (data?.docs?.public || []).map(m => ({title: m, link: m}))
    privateLinksList.value = (data?.docs?.private || []).map(m => ({title: m, link: m, private: true}))
  } catch (error) {
    $q.notify('获取失败! ' + error)
  }
}

const onPush = async () => {

  try {
    const resp = await build()

    if (!resp.ok) {
      const errorData = await resp.json()
      throw new Error(`API错误: ${resp.status} - ${errorData.message}`)
    }
    $q.notify('构建成功! ')
  } catch (error) {
    $q.notify('获取失败! ' + error)
  }
}
getDocsList()


</script>
