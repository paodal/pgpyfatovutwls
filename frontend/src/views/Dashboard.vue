<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div class="flex items-center">
            <router-link to="/" class="text-2xl font-bold text-gray-900 hover:text-gray-700">
              {{ $t('dashboard.title') }}
            </router-link>
          </div>
          
          <div class="flex items-center justify-center flex-1">
            <span class="text-xl font-bold text-primary-600">pgpyfatovutwls</span>
          </div>
          
          <div class="flex items-center space-x-4">
            <LanguageSelector />
            <div class="relative">
              <button @click="showUserMenu = !showUserMenu" class="flex items-center space-x-2 text-gray-700 hover:text-gray-900">
                <span>Admin</span>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
              </button>
              
              <div v-if="showUserMenu" class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50">
                <div v-if="user?.is_superuser">
                  <router-link to="/admin/plans" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                    {{ $t('admin.plans.title') }}
                  </router-link>
                  <button @click="openUsersModal" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                    {{ $t('admin.users.title') }}
                  </button>
                </div>
                <router-link v-if="!user?.is_superuser" to="/subscription" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                  {{ $t('dashboard.subscription.title') }}
                </router-link>
                <button @click="showPasswordModal = true" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                  {{ $t('dashboard.changePassword') }}
                </button>
                <button @click="logout" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                  {{ $t('auth.logout') }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Profile Card -->
        <div class="lg:col-span-1">
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                {{ $t('dashboard.profile.title') }}
              </h3>
              
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700">{{ $t('auth.fullName') }}</label>
                  <p class="mt-1 text-sm text-gray-900">{{ user?.full_name }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700">{{ $t('auth.email') }}</label>
                  <p class="mt-1 text-sm text-gray-900">{{ user?.email }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700">{{ $t('auth.language') }}</label>
                  <p class="mt-1 text-sm text-gray-900">{{ user?.language === 'it' ? 'Italiano' : 'English' }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700">Status</label>
                  <span class="mt-1 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" 
                        :class="user?.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                    {{ user?.is_active ? $t('dashboard.profile.active') : $t('dashboard.profile.inactive') }}
                  </span>
                </div>
                
                <div v-if="user?.is_superuser">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {{ $t('dashboard.profile.superuser') }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Subscription Card (only for regular users) -->
        <div v-if="!user?.is_superuser" class="lg:col-span-2">
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                {{ $t('dashboard.subscription.title') }}
              </h3>
              
              <div v-if="subscriptionLoading" class="text-center py-4">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              </div>
              
              <div v-else-if="currentSubscription" class="space-y-4">
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div class="flex items-center justify-between">
                    <div>
                      <h4 class="text-lg font-medium text-blue-900">
                        {{ currentSubscription.plan?.name || 'Premium Plan' }}
                      </h4>
                      <p class="text-sm text-blue-700">
                        {{ $t('dashboard.subscription.status') }}: {{ currentSubscription.status }}
                      </p>
                    </div>
                    <div class="text-right">
                      <p class="text-2xl font-bold text-blue-900">
                        €{{ currentSubscription.plan?.price || '29' }}
                      </p>
                      <p class="text-sm text-blue-700">/{{ $t('home.pricing.month') }}</p>
                    </div>
                  </div>
                  
                  <div class="mt-4 flex space-x-2">
                    <button @click="cancelSubscription" 
                            :disabled="cancelling"
                            class="px-4 py-2 bg-red-600 text-white text-sm rounded-md hover:bg-red-700 disabled:opacity-50">
                      {{ cancelling ? $t('dashboard.subscription.cancelling') : $t('dashboard.subscription.cancel') }}
                    </button>
                  </div>
                </div>
              </div>
              
              <div v-else class="text-center py-8">
                <div class="mb-4">
                  <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                  </svg>
                </div>
                <h4 class="text-lg font-medium text-gray-900 mb-2">
                  {{ $t('dashboard.subscription.noSubscription') }}
                </h4>
                <p class="text-gray-600 mb-6">
                  {{ $t('dashboard.subscription.upgradeMessage') }}
                </p>
                
                <!-- Subscription Plans -->
                <div v-if="plans.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div v-for="plan in plans" :key="plan.id" 
                       class="border border-gray-200 rounded-lg p-4 hover:border-blue-500 transition-colors">
                    <h5 class="font-medium text-gray-900">{{ plan.name }}</h5>
                    <p class="text-2xl font-bold text-gray-900 mt-2">
                      €{{ plan.price }}<span class="text-sm text-gray-500">/{{ $t('home.pricing.month') }}</span>
                    </p>
                    <p class="text-sm text-gray-600 mt-2">{{ plan.description }}</p>
                    <button @click="subscribe(plan.id)" 
                            :disabled="subscribing"
                            class="mt-4 w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50">
                      {{ subscribing ? $t('dashboard.subscription.subscribing') : $t('dashboard.subscription.subscribe') }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Admin Panel (only for superusers) -->
        <div v-if="user?.is_superuser" class="lg:col-span-2">
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                {{ $t('admin.panel.title') }}
              </h3>
              
              <div class="space-y-4">
                <div class="border border-gray-200 rounded-lg p-4">
                  <div class="flex items-center justify-between">
                    <div>
                      <h4 class="text-lg font-medium text-gray-900">
                        {{ $t('admin.plans.title') }}
                      </h4>
                      <p class="text-sm text-gray-600">
                        {{ $t('admin.plans.description') }}
                      </p>
                    </div>
                    <router-link to="/admin/plans" class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                      {{ $t('admin.plans.manage') }}
                    </router-link>
                  </div>
                </div>

                <div class="border border-gray-200 rounded-lg p-4">
                  <div class="flex items-center justify-between">
                    <div>
                      <h4 class="text-lg font-medium text-gray-900">
                        {{ $t('admin.users.title') }}
                      </h4>
                      <p class="text-sm text-gray-600">
                        {{ $t('admin.users.description') }}
                      </p>
                    </div>
                    <button @click="openUsersModal" class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                      {{ $t('admin.users.manage') }}
                    </button>
                  </div>
                </div>

                <div class="border border-gray-200 rounded-lg p-4">
                  <div class="flex items-center justify-between">
                    <div>
                      <h4 class="text-lg font-medium text-gray-900">
                        {{ $t('admin.analytics.title') }}
                      </h4>
                      <p class="text-sm text-gray-600">
                        {{ $t('admin.analytics.description') }}
                      </p>
                    </div>
                    <button disabled class="bg-gray-300 text-gray-500 px-4 py-2 rounded-md cursor-not-allowed">
                      {{ $t('admin.comingSoon') }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Quick Actions -->
      <div class="bg-white overflow-hidden shadow rounded-lg mt-6">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
            {{ $t('dashboard.quick_actions') }}
          </h3>
          
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <button class="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 text-left">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium text-gray-900">
                    {{ $t('dashboard.actions.new_project') }}
                  </p>
                  <p class="text-sm text-gray-500">
                    {{ $t('dashboard.actions.new_project_desc') }}
                  </p>
                </div>
              </div>
            </button>
            
            <button class="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 text-left">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium text-gray-900">
                    {{ $t('dashboard.actions.view_docs') }}
                  </p>
                  <p class="text-sm text-gray-500">
                    {{ $t('dashboard.actions.view_docs_desc') }}
                  </p>
                </div>
              </div>
            </button>
            
            <button v-if="!user?.is_superuser" class="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 text-left">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192L5.636 18.364M12 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium text-gray-900">
                    {{ $t('dashboard.actions.get_support') }}
                  </p>
                  <p class="text-sm text-gray-500">
                    {{ $t('dashboard.actions.get_support_desc') }}
                  </p>
                </div>
              </div>
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Password Change Modal -->
    <div v-if="showPasswordModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 class="text-lg font-medium text-gray-900 mb-4">{{ $t('dashboard.changePassword') }}</h3>
        
        <form @submit.prevent="changePassword" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Password attuale</label>
            <input v-model="passwordForm.currentPassword" type="password" required 
                   class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2">
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700">Nuova password</label>
            <input v-model="passwordForm.newPassword" type="password" required 
                   class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2">
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700">Conferma nuova password</label>
            <input v-model="passwordForm.confirmPassword" type="password" required 
                   class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2">
          </div>
          
          <div class="flex justify-end space-x-2 pt-4">
            <button type="button" @click="showPasswordModal = false" 
                    class="px-4 py-2 text-gray-600 hover:text-gray-800">
              Annulla
            </button>
            <button type="submit" :disabled="passwordChanging"
                    class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50">
              {{ passwordChanging ? 'Aggiornamento...' : 'Cambia Password' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Users Management Modal -->
    <div v-if="showUsersModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full min-w-[640px] max-w-5xl max-h-[80vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-4">
          <div class="flex items-center space-x-4">
            <h3 class="text-lg font-medium text-gray-900">{{ $t('admin.users.title') }}</h3>
            <button @click="openCreateUserModal" 
                    class="bg-green-600 text-white px-4 py-2 text-sm rounded-md hover:bg-green-700">
              + Crea Nuovo Utente
            </button>
          </div>
          <button @click="showUsersModal = false" 
                  class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <div v-if="usersLoading" class="text-center py-4">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
        
        <div v-else class="space-y-3">
          <div v-for="usr in allUsers" :key="usr.id" 
               :class="[
                 'border rounded-lg p-4 bg-white',
                 usr.is_superuser ? 'border-blue-300 bg-blue-50' : 'border-gray-200'
               ]">
            
            <!-- User Info and Controls -->
            <div class="grid grid-cols-12 gap-3">
              <!-- Basic Info (6 columns) -->
              <div class="col-span-6">
                <div class="space-y-2">
                  <!-- Status Toggles -->
                  <div class="flex items-center space-x-3">
                    <span class="text-xs text-gray-500">ID: {{ usr.id }}</span>
                    <div class="flex items-center space-x-1">
                      <input type="checkbox" v-model="usr.is_active" @change="updateUserStatus(usr)"
                             class="h-3 w-3 text-green-600 border-gray-300 rounded">
                      <span class="text-xs text-green-600">Attivo</span>
                    </div>
                    <div class="flex items-center space-x-1">
                      <input type="checkbox" v-model="usr.is_superuser" @change="updateUserStatus(usr)"
                             class="h-3 w-3 text-blue-600 border-gray-300 rounded">
                      <span class="text-xs text-blue-600">Admin</span>
                    </div>
                  </div>
                  <!-- User Fields -->
                  <input :value="usr.email" @input="usr.email = $event.target.value"
                         class="w-full border border-gray-300 rounded px-2 py-1 text-sm"
                         placeholder="Email">
                  <input :value="usr.full_name" @input="usr.full_name = $event.target.value"
                         class="w-full border border-gray-300 rounded px-2 py-1 text-sm"
                         placeholder="Nome completo">
                </div>
              </div>

              <!-- Subscription Section (4 columns) -->
              <div v-if="!usr.is_superuser" class="col-span-4">
                <div class="space-y-2">
                  <div class="text-xs font-medium text-gray-700">Abbonamento</div>
                  <select v-model="usr.selectedPlanId" class="text-xs border border-gray-300 rounded px-2 py-1 w-full">
                    <option value="">Nessun Piano</option>
                    <option v-for="plan in availablePlans" :key="plan.id" :value="plan.id">
                      {{ plan.name }} - €{{ plan.price }}
                    </option>
                  </select>
                </div>
              </div>
              <div v-else class="col-span-4">
                <div class="text-xs text-blue-600 font-medium">Utente Amministratore</div>
              </div>

              <!-- Action Buttons (2 columns) -->
              <div class="col-span-2 flex flex-col space-y-1">
                <button @click="openChangePasswordModal(usr)"
                        class="px-2 py-1 bg-yellow-500 text-white text-xs rounded hover:bg-yellow-600">
                  Password
                </button>
                <button @click="deleteUserAccount(usr.id, usr.full_name)"
                        class="px-2 py-1 bg-red-500 text-white text-xs rounded hover:bg-red-600">
                  Rimuovi
                </button>
              </div>
            </div>
            
            <!-- Save Button (Separate, larger) -->
            <div class="mt-3 pt-3 border-t border-gray-200">
              <button @click="updateUserStatus(usr)"
                      class="w-full px-4 py-2 bg-green-600 text-white text-sm rounded-md hover:bg-green-700 font-medium">
                Salva Modifiche
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- User Password Change Modal -->
    <div v-if="showUserPasswordModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 class="text-lg font-medium text-gray-900 mb-4">
          Cambia Password per {{ selectedUser?.full_name }}
        </h3>
        
        <form @submit.prevent="changeUserPassword" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Nuova password</label>
            <input v-model="userPasswordForm.newPassword" type="password" required 
                   class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2">
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700">Conferma nuova password</label>
            <input v-model="userPasswordForm.confirmPassword" type="password" required 
                   class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2">
          </div>
          
          <div class="flex justify-end space-x-2 pt-4">
            <button type="button" @click="showUserPasswordModal = false" 
                    class="px-4 py-2 text-gray-600 hover:text-gray-800">
              Annulla
            </button>
            <button type="submit" :disabled="userPasswordChanging"
                    class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50">
              {{ userPasswordChanging ? 'Aggiornamento...' : 'Cambia Password' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Create User Modal -->
    <div v-if="showCreateUserModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Crea Nuovo Utente</h3>
        
        <form @submit.prevent="createUser" class="space-y-4" :key="createUserFormKey">
          <div>
            <label class="block text-sm font-medium text-gray-700">Email</label>
            <input v-model="createUserForm.email" type="email" required autocomplete="off"
                   class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2">
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700">Nome completo</label>
            <input v-model="createUserForm.full_name" type="text" required autocomplete="off"
                   class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2">
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700">Password</label>
            <input v-model="createUserForm.password" type="password" required autocomplete="new-password"
                   class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2">
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700">Lingua</label>
            <select v-model="createUserForm.language" 
                    class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2">
              <option value="it">Italiano</option>
              <option value="en">English</option>
            </select>
          </div>
          
          <div class="flex items-center">
            <input v-model="createUserForm.is_superuser" type="checkbox" 
                   class="h-4 w-4 text-blue-600 border-gray-300 rounded">
            <label class="ml-2 block text-sm text-gray-700">
              Amministratore
            </label>
          </div>
          
          <!-- Subscription Section (only for non-admin users) -->
          <div v-if="!createUserForm.is_superuser">
            <label class="block text-sm font-medium text-gray-700">Abbonamento (opzionale)</label>
            <select v-model="createUserForm.selectedPlanId" 
                    class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2">
              <option value="">Nessun abbonamento</option>
              <option v-for="plan in availablePlans" :key="plan.id" :value="plan.id">
                {{ plan.name }} - €{{ plan.price }}/mese
              </option>
            </select>
          </div>
          
          <div class="flex justify-end space-x-2 pt-4">
            <button type="button" @click="closeCreateUserModal" 
                    class="px-4 py-2 text-gray-600 hover:text-gray-800">
              Annulla
            </button>
            <button type="submit" :disabled="userCreating"
                    class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50">
              {{ userCreating ? 'Creazione...' : 'Crea Utente' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useSubscriptionStore } from '../stores/subscription'
import LanguageSelector from '../components/LanguageSelector.vue'

const authStore = useAuthStore()
const subscriptionStore = useSubscriptionStore()

const showUserMenu = ref(false)
const subscriptionLoading = ref(false)
const subscribing = ref(false)
const cancelling = ref(false)
const showPasswordModal = ref(false)
const showUsersModal = ref(false)
const showUserPasswordModal = ref(false)
const showCreateUserModal = ref(false)
const createUserFormKey = ref(0)
const allUsers = ref([])
const usersLoading = ref(false)
const userCreating = ref(false)
const selectedUser = ref(null)
const availablePlans = ref([])
const createUserForm = ref({
  email: '',
  full_name: '',
  password: '',
  language: 'it',
  is_superuser: false,
  selectedPlanId: ''
})
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})
const userPasswordForm = ref({
  newPassword: '',
  confirmPassword: ''
})
const passwordChanging = ref(false)
const userPasswordChanging = ref(false)

const user = computed(() => authStore.user)
const currentSubscription = computed(() => subscriptionStore.currentSubscription)
const plans = computed(() => subscriptionStore.plans)

onMounted(async () => {
  await authStore.checkAuthStatus()
  
  subscriptionLoading.value = true
  await Promise.all([
    subscriptionStore.fetchCurrentSubscription(),
    subscriptionStore.fetchPlans()
  ])
  availablePlans.value = subscriptionStore.plans
  subscriptionLoading.value = false
})

const logout = () => {
  authStore.logout()
  showUserMenu.value = false
}

const subscribe = async (planId) => {
  subscribing.value = true
  try {
    await subscriptionStore.createCheckout(planId)
  } catch (error) {
    console.error('Subscription failed:', error)
  } finally {
    subscribing.value = false
  }
}

const cancelSubscription = async () => {
  if (!currentSubscription.value?.id) return
  
  cancelling.value = true
  try {
    const result = await subscriptionStore.cancelSubscription(currentSubscription.value.id)
    if (result.success) {
      // Subscription cancelled successfully
    }
  } catch (error) {
    console.error('Cancellation failed:', error)
  } finally {
    cancelling.value = false
  }
}

const changePassword = async () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    alert('Le password non corrispondono')
    return
  }
  
  passwordChanging.value = true
  try {
    await authStore.changePassword(passwordForm.value.currentPassword, passwordForm.value.newPassword)
    showPasswordModal.value = false
    passwordForm.value = { currentPassword: '', newPassword: '', confirmPassword: '' }
    alert('Password cambiata con successo')
  } catch (error) {
    console.error('Password change failed:', error)
    alert('Errore nel cambio password')
  } finally {
    passwordChanging.value = false
  }
}

const openUsersModal = async () => {
  showUsersModal.value = true
  await loadUsers()
}

const loadUsers = async () => {
  if (!user.value?.is_superuser) return
  
  usersLoading.value = true
  try {
    allUsers.value = await authStore.getAllUsers()
    // Initialize selectedPlanId for each user
    allUsers.value.forEach(usr => {
      usr.selectedPlanId = usr.subscription?.plan_id || ''
    })
  } catch (error) {
    console.error('Failed to load users:', error)
  } finally {
    usersLoading.value = false
  }
}


const updateUserStatus = async (usr) => {
  try {
    // Update user basic info
    await authStore.updateUser(usr.id, { 
      email: usr.email, 
      full_name: usr.full_name,
      is_superuser: usr.is_superuser,
      is_active: usr.is_active
    })
    
    // Handle subscription changes (only for non-admin users)
    if (!usr.is_superuser) {
      const currentSubscriptionId = usr.subscription?.plan_id
      const selectedPlanId = usr.selectedPlanId
      
      // If subscription changed
      if (currentSubscriptionId !== selectedPlanId) {
        if (selectedPlanId === '' || selectedPlanId === null) {
          // Cancel subscription if "Nessun Piano" selected
          if (currentSubscriptionId) {
            await authStore.cancelUserSubscription(usr.id)
          }
        } else {
          // Set new subscription
          await authStore.setUserSubscription(usr.id, selectedPlanId)
        }
      }
    }
    
    await loadUsers() // Reload users
    alert(`Utente ${usr.full_name} aggiornato con successo`)
  } catch (error) {
    console.error('Failed to update user:', error)
    alert('Errore nell\'aggiornamento utente')
    // Reload to revert changes
    await loadUsers()
  }
}

const openChangePasswordModal = (user) => {
  selectedUser.value = user
  userPasswordForm.value = { newPassword: '', confirmPassword: '' }
  showUserPasswordModal.value = true
}

const changeUserPassword = async () => {
  if (userPasswordForm.value.newPassword !== userPasswordForm.value.confirmPassword) {
    alert('Le password non corrispondono')
    return
  }
  
  userPasswordChanging.value = true
  try {
    await authStore.adminChangePassword(selectedUser.value.id, userPasswordForm.value.newPassword)
    showUserPasswordModal.value = false
    alert('Password utente cambiata con successo')
  } catch (error) {
    console.error('Failed to change user password:', error)
    alert('Errore nel cambio password utente')
  } finally {
    userPasswordChanging.value = false
  }
}

const deleteUserAccount = async (userId, userName) => {
  if (!confirm(`Sei sicuro di voler eliminare l'utente ${userName}? Questa azione non può essere annullata.`)) {
    return
  }
  
  try {
    await authStore.deleteUser(userId)
    await loadUsers()
    alert('Utente eliminato con successo')
  } catch (error) {
    console.error('Failed to delete user:', error)
    alert('Errore nell\'eliminazione utente')
  }
}


const openCreateUserModal = () => {
  // Reset form to empty values and force re-render
  createUserForm.value = {
    email: '',
    full_name: '',
    password: '',
    language: 'it',
    is_superuser: false,
    selectedPlanId: ''
  }
  createUserFormKey.value++
  showCreateUserModal.value = true
}

const closeCreateUserModal = () => {
  // Reset form when closing
  createUserForm.value = {
    email: '',
    full_name: '',
    password: '',
    language: 'it',
    is_superuser: false,
    selectedPlanId: ''
  }
  createUserFormKey.value++
  showCreateUserModal.value = false
}

const createUser = async () => {
  userCreating.value = true
  try {
    // Create the user first
    const newUser = await authStore.createUser(createUserForm.value)
    
    // If a subscription plan is selected and user is not admin, assign the subscription
    if (createUserForm.value.selectedPlanId && !createUserForm.value.is_superuser) {
      try {
        await authStore.setUserSubscription(newUser.id, createUserForm.value.selectedPlanId)
      } catch (subscriptionError) {
        console.error('Failed to set subscription:', subscriptionError)
        alert('Utente creato con successo, ma errore nell\'assegnazione abbonamento')
      }
    }
    
    closeCreateUserModal()
    await loadUsers()
    alert('Utente creato con successo')
  } catch (error) {
    console.error('Failed to create user:', error)
    alert('Errore nella creazione utente')
  } finally {
    userCreating.value = false
  }
}

// Close user menu when clicking outside
document.addEventListener('click', (e) => {
  if (!e.target.closest('.relative')) {
    showUserMenu.value = false
  }
})
</script>