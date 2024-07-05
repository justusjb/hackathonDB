declare module 'svelte-select' {
    import { SvelteComponentTyped } from 'svelte';

    interface SelectProps {
        items: any[];
        selectedValue?: any;
        isMulti?: boolean;
        placeholder?: string;
        [key: string]: any;
    }

    export default class Select extends SvelteComponentTyped<SelectProps> {}
}