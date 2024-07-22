<script lang="ts">
  import { fly } from 'svelte/transition';

  export let show = false;
  export let type: 'success' | 'error' = 'success';
  export let message = '';
</script>

{#if show}
  <div class="fixed inset-0 flex items-end justify-center px-4 py-6 pointer-events-none sm:p-6 sm:items-start sm:justify-end z-50">
    <div
      class="max-w-sm w-full alert {type === 'success' ? 'alert-success' : 'alert-error'} shadow-lg"
      role="alert"
      transition:fly="{{ y: 50, duration: 300 }}"
    >
      {#if type === 'success'}
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
      {:else}
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
      {/if}
      <span>{message}</span>
    </div>
  </div>
{/if}