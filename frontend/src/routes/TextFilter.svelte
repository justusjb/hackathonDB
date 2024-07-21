<script>
  import {darkMode} from "../stores/darkMode.js";

  export let placeholder = "Search...";
  export let value = "";

  $: isDarkMode = $darkMode;

  $: backgroundColor = isDarkMode ? 'rgb(31, 41, 55)' : 'rgb(255, 255, 255)';
  $: borderColor = isDarkMode ? 'rgb(75, 85, 99)' : 'rgb(209, 213, 219)';
  $: textColor = isDarkMode ? 'rgb(243, 244, 246)' : 'rgb(17, 24, 39)';
  $: placeholderColor = isDarkMode ? 'rgb(156, 163, 175)' : 'rgb(107, 114, 128)';
  $: borderHoverColor = isDarkMode ? 'rgb(107, 114, 128)' : 'rgb(107, 114, 128)';
  $: borderFocusColor = 'rgb(96, 165, 250)';

  let isFocused = false;

  function handleFocus() {
    isFocused = true;
  }

  function handleBlur() {
    isFocused = false;
  }
</script>

<div class="mb-4">
    <h3 class="font-bold mb-2 {isDarkMode ? 'text-gray-300' : 'text-black'}">Text Search</h3>
<div
  class="custom-select svelte-select-wrapper"
  class:focused={isFocused}
  aria-haspopup="listbox"
  aria-expanded="false"
  style="
    --background: {backgroundColor};
    --border-color: {borderColor};
    --border-hover-color: {borderHoverColor};
    --border-focus-color: {borderFocusColor};
    --input-color: {textColor};
    --placeholder-color: {placeholderColor};
  "
>
  <div class="value-container">
      <input
        type="text"
        {placeholder}
        bind:value
        class="svelte-select-input"
        style="color: var(--input-color);"
        on:input
        on:focus={handleFocus}
        on:blur={handleBlur}
      />
    </div>
</div>
</div>

<style>
  .svelte-select-wrapper {
    position: relative;
    display: flex;
    align-items: stretch;
    border-radius: 6px;
    min-height: 45.8097px;
    font-family: ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
    font-size: 16px;
    line-height: 24px;
    box-sizing: border-box;
    background-color: var(--background);
  }

  .svelte-select-wrapper::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 6px;
    border: 1px solid var(--border-color);
    pointer-events: none;
    transition: border-color 0.1s;
  }

  .svelte-select-wrapper:hover::before {
    border-color: var(--border-hover-color);
  }

  .svelte-select-wrapper.focused::before {
    border-color: var(--border-focus-color);
  }

.value-container {
  align-items: center;
  display: flex;
  flex: 1 1 0;
  padding: 0 16px;
  position: relative;
  overflow: hidden;
  box-sizing: border-box;
  cursor: text;
}

.svelte-select-input {
  flex-grow: 1;
  background-color: transparent;
  border: none;
  font-size: 16px;
  line-height: 24px;
  padding: 5px 16px;
  min-width: calc(100% + 32px);
  height: 100%;
  cursor: text;
  margin-left: -16px;
}

  .svelte-select-input::placeholder {
    color: var(--placeholder-color);
    opacity: 1;
  }

  .svelte-select-input:focus {
    outline: none;
  }
</style>