<template>
  <div
    :class="item.row_background_color"
    class="flex flex-row flex-nowrap pv2">
    <img
      :src="item.img"
      class="search-icon-size ph2">
    <div
      class="ph2">
      <h3
        class="search-title-color mv0 f5 fontweight-400">{{ item.name }}</h3>
      <small
        class="info-color f7">
        {{ item.id_description }}: {{ item.id }}<br>
      </small>
      <small
        class="info-color f7">
        {{ item.extra_info }}: {{ item.extra_info_content }}
      </small>
      <template
        v-if="item.filter_options">
        <br><span class="info-color f6">Show:</span>
        <a
          v-for="filter in item.filter_options"
          :key="filter"
          href="#"
          class="selector-depth-color link no-underline underline-hover f6"
          @click="$emit('select-filter', filter)">{{ filter + '  ' }}
        </a>
      </template>
    </div>
    <div
      class="selection-button-margin">
      <a
        :href="item.url"
        class="f6 link ba br2 ph2 pv2 mr2 dib mt1">Select
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: "SelectableItem",
  props: {
    item: {
      type: Object,
      default() {
        return null;
      },
    },
  },
  data() {
    return {
    };
  },
  methods: {
  },
};
</script>
