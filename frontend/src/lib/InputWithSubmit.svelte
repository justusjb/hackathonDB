<script lang="ts">
  import * as acorn from "acorn";

  export let placeholder = "";
  export let buttonText = "Submit";
  export let description = "";

  let inputValue = "";

  //export let onSubmit = () => {};
  export let onSubmit = (value: string) => {value};


  let inputElement: any;
  let isButtonClicked = true;
  let isButtonAnimating = false;

  function handleMousedown() {
    isButtonClicked = true;
    if (inputElement) {
      inputElement.blur();
    }
    animateButton();
  }

    function handleButtonclick() {
        if (inputValue.trim()) {
        onSubmit(inputValue);
        inputValue = "";
      }
    }

  function handleInputFocus() {
    isButtonClicked = false;
  }

  function animateButton() {
    isButtonAnimating = true;
    setTimeout(() => {
      isButtonAnimating = false;
    }, 100); // Match this duration with the CSS transition duration
  }
</script>

<div class="mb-2">
  <div class="join w-full rounded-lg {isButtonClicked ? '' : 'focus-within:ring-2 focus-within:ring-blue-400 dark:focus-within:ring-gray-400'} overflow-hidden">
    <input
      bind:this={inputElement}
      bind:value={inputValue}
      type="text"
      placeholder={placeholder}
      on:focus={handleInputFocus}

      class="input join-item w-full pr-4 focus:outline-none border-r-0 focus:border-transparent text-black bg-white dark:bg-gray-800 dark:border-gray-600 dark:focus:border-transparent dark:placeholder-gray-400 dark:text-white"
    />
    <button
      class="btn join-item rounded-r-lg bg-blue-900 disabled:bg-blue-900 disabled:text-white text-white border-blue-900 betterhover:hover:bg-blue-700 betterhover:hover:border-blue-700 focus:outline-none dark:bg-gray-600 dark:border-gray-600 dark:text-white dark:betterhover:hover:bg-gray-500 dark:betterhover:hover:border-gray-500 transition-transform duration-100 {isButtonAnimating ? 'scale-95' : ''}"
      on:mousedown={handleMousedown}
      on:click={handleButtonclick}
      disabled={!inputValue.trim()}
    >
      {buttonText}
    </button>
  </div>
</div>
<p class="text-gray-500 dark:text-gray-400 text-sm mb-6">{description}</p>

