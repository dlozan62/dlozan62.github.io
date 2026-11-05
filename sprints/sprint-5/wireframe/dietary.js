'use strict';

// Fictional examples demonstrate filtering; no real restaurant claims are made.
const dietary = (() => {
  const menus = {
    venue1: [
      { name: 'Example veggie bowl', diets: ['vegan', 'vegetarian', 'gluten-free'], allergens: [], ingredients: 'Rice, beans, vegetables (fictional recipe)', available: true },
      { name: 'Example cheese wrap', diets: ['vegetarian'], allergens: ['milk', 'wheat'], ingredients: 'Tortilla, cheese, vegetables (fictional recipe)', available: false },
      { name: 'Example sesame tofu bowl', diets: ['vegan', 'vegetarian'], allergens: ['soy', 'sesame', 'wheat'], ingredients: 'Tofu, sesame, wheat-containing sauce (fictional recipe)', available: true },
    ],
    venue2: [
      { name: 'Example vegetable soup', diets: ['vegan', 'vegetarian', 'gluten-free'], allergens: [], ingredients: 'Vegetables, water, herbs (fictional recipe)', available: null },
      { name: 'Example cafe special', diets: null, allergens: null, ingredients: 'Unknown — confirm with staff', available: null },
    ],
    venue3: [
      { name: 'Chicken sandwich — unverified example', diets: null, allergens: null, ingredients: 'Unknown — confirm with staff', available: true },
      { name: '[Item name] — unverified example', diets: null, allergens: null, ingredients: 'Unknown — confirm with staff', available: false },
    ],
  };

  function matches(item, filters, venueOpen) {
    if (filters.diet && (!item.diets || !item.diets.includes(filters.diet))) return false;
    if (filters.avoid.length && (!item.allergens || filters.avoid.some(allergen => item.allergens.includes(allergen)))) return false;
    if (filters.inStock && (!venueOpen || item.available !== true)) return false;
    return true;
  }

  return { menus, matches };
})();

if (typeof module !== 'undefined' && module.exports) module.exports = dietary;
