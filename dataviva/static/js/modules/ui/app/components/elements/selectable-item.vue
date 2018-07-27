<template>
  <div class="flex flex-row flex-nowrap pv2" 
    v-bind:class="item.row_background_color"> <img class="search-icon-size ph2" 
    v-bind:src="item.img">
    <div class="ph2">
      <h3 class="search-title-color mv0 f5 fontweight-400">{{item.name}}</h3>
      <small 
        class="info-color f7">
        {{item.id_description}}: {{item.id}}<br/>
      </small>
      <small 
        class="info-color f7">
        {{item.extra_info}}: {{item.extra_info_content}}
      </small>
      <template 
        v-if="item.filter_options">
        <br><span class="info-color f6">Show:</span> 
        <a 
          href="#" 
          class="selector-depth-color link no-underline underline-hover f6"
          v-on:click="$emit('select-filter', filter)"
          v-for="filter in item.filter_options">{{filter + '  '}}
        </a>
      </template>
    </div>    
    <div class="selection-button-margin">
      <a 
         class="f6 link ba br2 ph2 pv2 mr2 dib mt1" 
         v-bind:href="item.url">Select
      </a>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'SelectableItem',
    props: ['item'],
    data() {
      return {
      };
    },
    methods: {
    },
  };
</script>