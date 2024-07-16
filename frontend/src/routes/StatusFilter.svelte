<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import { writable, get } from 'svelte/store';

    const selectedStatuses = writable<Set<string>>(new Set());

    const announcedChecked = writable(false);
    const applicationsOpenChecked = writable(false);
    const applicationsClosedChecked = writable(false);
    const expectedChecked = writable(false);

    // Dispatch events to notify the parent component of changes
    const dispatch = createEventDispatcher();

    function toggleStatus(status: string) {
        selectedStatuses.update(set => {
            if (set.has(status)) {
                set.delete(status);
            } else {
                set.add(status);
            }
            return new Set(set);
        });

        // Notify the parent component of the change
        dispatch('statusUpdate', { statuses: get(selectedStatuses) });
    }

    // Subscribe to changes in selectedStatuses to update checkbox states
    selectedStatuses.subscribe(statuses => {
        announcedChecked.set(statuses.has('announced'));
        applicationsOpenChecked.set(statuses.has('applications_open'));
        applicationsClosedChecked.set(statuses.has('applications_closed'));
        expectedChecked.set(statuses.has('expected'));
    });
</script>

<div class="mb-4">
    <label class="inline-flex items-center mr-4">
        <input type="checkbox" class="form-checkbox text-yellow-500 h-5 w-5" bind:checked={$announcedChecked} on:change={() => toggleStatus('announced')}>
        <span class="ml-2 text-gray-700 dark:text-gray-400">Announced</span>
    </label>
    <label class="inline-flex items-center mr-4">
        <input type="checkbox" class="form-checkbox text-green-600 h-5 w-5" bind:checked={$applicationsOpenChecked} on:change={() => toggleStatus('applications_open')}>
        <span class="ml-2 text-gray-700  dark:text-gray-400">Applications Open</span>
    </label>
    <label class="inline-flex items-center mr-4">
        <input type="checkbox" class="form-checkbox text-red-600 h-5 w-5" bind:checked={$applicationsClosedChecked} on:change={() => toggleStatus('applications_closed')}>
        <span class="ml-2 text-gray-700  dark:text-gray-400">Applications Closed</span>
    </label>
    <label class="inline-flex items-center mr-4">
        <input type="checkbox" class="form-checkbox text-gray-400 h-5 w-5" bind:checked={$expectedChecked} on:change={() => toggleStatus('expected')}>
        <span class="ml-2 text-gray-700 dark:text-gray-400">Expected</span>
    </label>
</div>

<style>
    .form-checkbox {
        margin-right: 8px;
    }
</style>