<script>
  export let placeholder = "";
  export let buttonText = "Submit";
  export let inputType = "text";
  export let description = "";
  export let onSubmit = () => {};
</script>

<div class="relative mb-2">
  <input
    type={inputType}
    placeholder={placeholder}
    class="border p-4 w-full rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 pr-24"
    style="padding-right: 80px;"
  />
  <button class="absolute right-0 top-0 h-full custom-button" on:click={onSubmit}>
    {buttonText}
  </button>
</div>
<p class="text-gray-500 text-sm mb-6">{description}</p>

<style>
    .custom-button {
        background-color: #1E3A8A;
        border: 2px solid #1E3A8A;
        color: white;
        border-radius: 0 0.5rem 0.5rem 0;
        padding: 0.5rem 1rem;
        transition: background-color 0.3s, border-color 0.3s;
    }

    .custom-button:hover {
        background-color: #1D4ED8;
        border-color: #1D4ED8;
    }

    .custom-button:focus {
        outline: none;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
    }
</style>