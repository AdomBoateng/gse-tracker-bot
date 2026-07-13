<template>
  <div class="seg" :style="block ? 'display:flex;width:100%' : ''" role="group" aria-label="Layout">
    <label
      class="seg-opt"
      :class="{ 'is-active': modelValue === '1a' }"
      :style="block ? 'flex:1;justify-content:center' : ''"
      title="Ledger layout"
      @click="$emit('update:modelValue', '1a')"
    >
      Ledger
    </label>
    <label
      class="seg-opt"
      :class="{ 'is-active': modelValue === '1b' }"
      :style="block ? 'flex:1;justify-content:center' : ''"
      title="Split-terminal layout"
      @click="$emit('update:modelValue', '1b')"
    >
      Terminal
    </label>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    modelValue: "1a" | "1b";
    block?: boolean;
  }>(),
  { block: false },
);

defineEmits<{ "update:modelValue": [value: "1a" | "1b"] }>();
</script>
