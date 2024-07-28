<template>
  <div class="overflow-hidden shadow-2 rounded-borders">
    <q-drawer
        v-model="drawerOpen"
        show-if-above

        :mini="!drawerOpen || miniState"
        @click.capture="drawerClick"

        :width="200"
        :breakpoint="500"
        bordered
        :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-3'"
    >
      <q-scroll-area class="fit" :horizontal-thumb-style="{ opacity: 0 }">
        <q-list bordered class="rounded-borders">
          <q-expansion-item
              v-for="item in menuData"
              :key="item.label"
              :expand-separator="true"
              :icon="item.icon"
              :label="item.label"
              :caption="item.caption || ''"
          >
            <q-list padding class="rounded-borders text-primary">
              <q-item
                  v-for="child in item.children"
                  :key="child.title"
                  clickable
                  v-ripple
                  :active="link === child.title"
                  @click="link = child.title; menuClick()"
                  active-class="my-menu-link"
              >
                <q-item-section avatar>
                  <q-icon :name="child.icon"/>
                </q-item-section>
                <q-item-section>
                  {{ child.title }}
                </q-item-section>
              </q-item>
            </q-list>
            <template v-if="!item.children || item.children.length === 0">
              <q-card>
                <q-card-section>
                  {{ item.defaultContent || 'No content available.' }}
                </q-card-section>
              </q-card>
            </template>
          </q-expansion-item>
        </q-list>
      </q-scroll-area>

    </q-drawer>
  </div>
</template>
<script>
export default {
  props: {
    menuData: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      drawerOpen: true,
      miniState: false,
      link: "home"
    }
  },
  mounted() {
    this.debugExpansionItems();
  },
  methods: {
    debugExpansionItems() {
      console.log('renderData:', this.menuData);
    },
    drawerClick(e) {
      if (this.miniState) {
        e.stopPropagation()
      }
    },
    toggleDrawer() {
      this.drawerOpen = !this.drawerOpen
      console.log("toggleDrawer", this.drawerOpen)
      this.$emit("drawer-toggle", this.drawerOpen)
    },
    toggleMini() {
      this.miniState = !this.miniState
      console.log("toggleMini", this.miniState)
      this.$emit("mini-toggle", this.miniState)
    },
    menuClick() {
      console.log("menuClick", this.link)
      this.$emit("menu-click", this.link)
    },
    testArg(arg) {
      console.log("testArg", arg)
    }
  }
};
</script>

<style lscoped>
.my-menu-link {
  color: white;
  background: #F2C037
}
</style>