<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import { writable, get } from 'svelte/store';
    import { darkMode } from '../stores/darkMode.js';

    const selectedStatuses = writable<Set<string>>(new Set());

    const announcedChecked = writable(false);
    const applicationsOpenChecked = writable(false);
    const applicationsClosedChecked = writable(false);
    const expectedChecked = writable(false);

    $: isDarkMode = $darkMode;

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

    <h3 class="font-bold {isDarkMode ? 'text-gray-300' : 'text-black'}">Application Status</h3>
<div class="flex flex-wrap gap-4 my-2">
    <div class="form-control">
        <label class="label cursor-pointer">
            <input type="checkbox" class="checkbox checkbox-warning mr-2"
                   bind:checked={$announcedChecked}
                   on:change={() => toggleStatus('announced')}/>
            <span class="label-text text-gray-800 dark:text-gray-300">Announced</span>
        </label>
    </div>
    <div class="form-control">
        <label class="label cursor-pointer">
            <input type="checkbox" class="checkbox checkbox-success mr-2"
                   bind:checked={$applicationsOpenChecked}
                   on:change={() => toggleStatus('applications_open')}/>
            <span class="label-text text-gray-800 dark:text-gray-300">Applications Open</span>
        </label>
    </div>
    <div class="form-control">
        <label class="label cursor-pointer">
            <input type="checkbox" class="checkbox checkbox-error mr-2"
                   bind:checked={$applicationsClosedChecked}
                   on:change={() => toggleStatus('applications_closed')}/>
            <span class="label-text text-gray-800 dark:text-gray-300">Applications Closed</span>
        </label>
    </div>
    <div class="form-control">
        <label class="label cursor-pointer">
            <input type="checkbox" class="checkbox checkbox-neutral border-gray-600 dark:border-gray-600 mr-2"
                   bind:checked={$expectedChecked}
                   on:change={() => toggleStatus('expected')}/>
            <span class="label-text text-gray-800 dark:text-gray-300">Expected</span>
        </label>
    </div>
</div>