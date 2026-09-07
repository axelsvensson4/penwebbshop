<template>
  <h1 class="text-h4 mb-2">Användare</h1>
  <p class="text-medium-emphasis mb-8">Hantera användarkonton och behörigheter.</p>

  <v-alert v-if="store.error" class="mb-5" type="error" variant="tonal">{{ store.error }}</v-alert>

  <v-list border>
    <v-list-item
      v-for="user in store.users"
      :key="user.id"
      :subtitle="`${user.username} · ${user.role} · ${user.active ? 'Aktiv' : 'Portad'}`"
      :title="user.name || user.username"
    >
      <template #append>
        <v-menu v-if="user.id !== auth.user?.id">
          <template #activator="{ props }">
            <v-btn v-bind="props" icon="mdi-dots-vertical" variant="text" />
          </template>

          <v-list min-width="180">
            <v-list-item
              :prepend-icon="user.active ? 'mdi-account-cancel-outline' : 'mdi-account-check-outline'"
              :title="user.active ? 'Porta konto' : 'Aktivera konto'"
              @click="store.toggleBan(user.id)"
            />

            <v-list-item
              base-color="error"
              prepend-icon="mdi-delete-outline"
              title="Radera konto"
              @click="selectedUser = user"
            />
          </v-list>
        </v-menu>
      </template>
    </v-list-item>

    <v-list-item v-if="store.users.length === 0" title="Inga användare ännu." />
  </v-list>

  <v-dialog v-model="deleteDialogOpen" max-width="460">
    <v-card class="pa-6">
      <h2 class="text-h6 mb-3">Radera konto?</h2>
      <p>Du är på väg att radera kontot för <strong>{{ selectedUser?.name || selectedUser?.username }}</strong>. Detta kan inte ångras.</p>

      <div class="d-flex justify-end ga-3 mt-5">
        <v-btn variant="text" @click="selectedUser = null">Avbryt</v-btn>
        <v-btn color="error" @click="confirmDelete">Radera konto</v-btn>
      </div>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
  import type { AdminUser } from '@/types/admin-user'
  import { computed, onMounted, ref } from 'vue'
  import { useAdminUsersStore } from '@/stores/admin-users'
  import { useAuthStore } from '@/stores/auth'

  const auth = useAuthStore()
  const store = useAdminUsersStore()
  const selectedUser = ref<AdminUser | null>(null)
  const deleteDialogOpen = computed({
    get: () => selectedUser.value !== null,
    set: value => {
      if (!value) selectedUser.value = null
    },
  })

  async function confirmDelete () {
    if (!selectedUser.value) return
    await store.remove(selectedUser.value.id)
    selectedUser.value = null
  }

  onMounted(store.load)
</script>
