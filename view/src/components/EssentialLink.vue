<template>
  <q-item
    clickable
    @click="to(props.link)"
  >
    <q-item-section
      v-if="props.icon"
      avatar
    >
      <q-icon :name="props.icon" />
    </q-item-section>

    <q-item-section>
      <q-item-label>{{ props.title }}</q-item-label>
    </q-item-section>
  </q-item>
</template>

<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
  title: {
    type: String,
    required: true
  },

  private: {
    type: Boolean,
    default: false
  },

  link: {
    type: String,
    default: '#'
  },

  icon: {
    type: String,
    default: ''
  }
})
const $r = useRouter()

function to(link) {
  if(props.private) {
    $r.push({path: `/${link}`, query: {private:  true}})
    return
  }
  $r.push(`/${link}`)
}
</script>
