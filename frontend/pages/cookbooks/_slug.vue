<template>
  <v-container v-if="book" fluid>
    <v-app-bar color="transparent" flat class="mt-n1 rounded">
      <v-icon large left> {{ $globals.icons.pages }} </v-icon>
      <v-toolbar-title class="headline"> {{ book.name }} </v-toolbar-title>
    </v-app-bar>
    <v-card flat>
      <v-card-text class="py-0">
        {{ book.description }}
      </v-card-text>
    </v-card>

    <v-container class="pa-0">
      <RecipeCardSection
        class="mb-5 mx-1"
        :recipes="recipes"
        :query="{ cookbook: slug }"
        @sortRecipes="assignSorted"
        @replaceRecipes="replaceRecipes"
        @appendRecipes="appendRecipes"
        @delete="removeRecipe"
      />
    </v-container>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, useRoute, ref, useMeta } from "@nuxtjs/composition-api";
import { useLazyRecipes } from "~/composables/recipes";
import RecipeCardSection from "@/components/Domain/Recipe/RecipeCardSection.vue";
import { useCookbook } from "~/composables/use-group-cookbooks";

export default defineComponent({
  components: { RecipeCardSection },
  setup() {
    const { recipes, appendRecipes, assignSorted, removeRecipe, replaceRecipes } = useLazyRecipes();

    const route = useRoute();
    const slug = route.value.params.slug;
    const { getOne } = useCookbook();

    const tab = ref(null);
    const book = getOne(slug);

    useMeta(() => {
      return {
        title: book?.value?.name || "Cookbook",
      };
    });

    return {
      book,
      slug,
      tab,
      appendRecipes,
      assignSorted,
      recipes,
      removeRecipe,
      replaceRecipes,
    };
  },
  head: {}, // Must include for useMeta
});
</script>
