<script>
  import { onMount } from 'svelte';
  
  let containerStatus = '';
  let error = '';
  
  onMount(async () => {
    try {
      const response = await fetch('/api/container/status');
      const data = await response.json();
      containerStatus = data.status;
    } catch (err) {
      error = 'Failed to fetch container status';
      console.error(err);
    }
  });
</script>

<div class="container-status">
  {#if error}
    <p class="error">{error}</p>
  {:else}
    <p>Container Status: {containerStatus}</p>
  {/if}
</div>

<style>
  .container-status {
    padding: 1rem;
  }
  
  .error {
    color: red;
  }
</style>
