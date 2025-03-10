{/* ContainerSettings.svelte */}
<script lang="ts">
  import { onMount } from 'svelte';
  import { Button } from '$lib/components/ui/button';
  import { Input } from '$lib/components/ui/input';
  import { Label } from '$lib/components/ui/label';
  import { Card } from '$lib/components/ui/card';
  import { toast } from '$lib/components/ui/toaster';

  let containerStatus = '';
  let containerVersion = '';
  let isUpdating = false;
  let isRestarting = false;

  async function fetchContainerStatus() {
    try {
      const response = await fetch('/api/container/status');
      const data = await response.json();
      containerStatus = data.status;
      containerVersion = data.version;
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to fetch container status',
        variant: 'destructive'
      });
    }
  }

  async function handleUpdate() {
    isUpdating = true;
    try {
      const response = await fetch('/api/container/update', {
        method: 'POST'
      });
      const data = await response.json();
      if (data.success) {
        toast({
          title: 'Success',
          description: 'Container updated successfully'
        });
        await fetchContainerStatus();
      } else {
        throw new Error(data.message);
      }
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to update container',
        variant: 'destructive'
      });
    } finally {
      isUpdating = false;
    }
  }

  async function handleRestart() {
    isRestarting = true;
    try {
      const response = await fetch('/api/container/restart', {
        method: 'POST'
      });
      const data = await response.json();
      if (data.success) {
        toast({
          title: 'Success',
          description: 'Container restarted successfully'
        });
        await fetchContainerStatus();
      } else {
        throw new Error(data.message);
      }
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to restart container',
        variant: 'destructive'
      });
    } finally {
      isRestarting = false;
    }
  }

  onMount(() => {
    fetchContainerStatus();
  });
</script>

<Card class="p-6">
  <h2 class="text-2xl font-bold mb-4">Container Management</h2>
  
  <div class="space-y-4">
    <div class="flex flex-col gap-2">
      <Label>Status</Label>
      <Input value={containerStatus} readonly />
    </div>

    <div class="flex flex-col gap-2">
      <Label>Version</Label>
      <Input value={containerVersion} readonly />
    </div>

    <div class="flex gap-4 mt-4">
      <Button 
        variant="primary" 
        disabled={isUpdating} 
        on:click={handleUpdate}
      >
        {isUpdating ? 'Updating...' : 'Update Container'}
      </Button>

      <Button 
        variant="secondary" 
        disabled={isRestarting} 
        on:click={handleRestart}
      >
        {isRestarting ? 'Restarting...' : 'Restart Container'}
      </Button>
    </div>
  </div>
</Card> 