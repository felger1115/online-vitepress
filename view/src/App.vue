<template>
  <router-view />
</template>

<script setup>
import { provide, ref } from 'vue';

let authid = ref('')

provide('authid', authid)

const root_key = 'JD9n9pvZkwBsxkctgyhKRhmT58PG4rDaU51K'

function getkey() {
  fetch('/root/api/getkey', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'secret': root_key
    }
  })
  .then(res => {
    return res.json()
  })
  .then(resp => {
    authid.value = resp.key
  })
}
getkey()

function build() {
  return fetch('/root/api/build', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'secret': root_key
    }
  })
}
provide('build', build)

</script>
<style>
.row {
  display: flex;
  flex-direction: row;

}
.column {
  display: flex;
  flex-direction: column;
}
.row-center {
  display: flex;
  align-items: center;
  user-select: none;
}
</style>
