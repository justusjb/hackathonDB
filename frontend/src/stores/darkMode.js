// src/stores/darkMode.js
import { writable } from 'svelte/store';

const isBrowser = typeof window !== 'undefined';
const initialDarkMode = isBrowser ? localStorage.getItem('darkMode') === 'true' : false;

export const darkMode = writable(initialDarkMode);

if (isBrowser) {
  darkMode.subscribe(value => {
    localStorage.setItem('darkMode', value.toString());
    if (value) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  });
}