<template>
  <div style="min-height: 100vh; display: flex; flex-direction: column; background: var(--color-bg)">
    <main style="flex: 1">
      <router-view />
    </main>
    <footer
      class="text-muted"
      style="border-top: 2px solid var(--color-divider); padding: var(--space-4) var(--space-6); text-align: center; font-size: 12px"
    >
      © 2026 GSE Tracker · Data via afx.kwayisi.org
    </footer>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";
</script>
