<template>
  <input class="input"
           :value="modelValue"
           @input="$emit('update:modelValue', $event.target.value)"
           :type="inputType"
           :placeholder="placeholder"
           @click="togglePassword"
    />
</template>

<script>
export default {
  props: {
    modelValue: {
      required: true,
      type: String
    },
    isPassword: {
      required: false,
      type: Boolean,
      default: false
    },
    placeholder: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      showPassword: true
    };
  },
  computed: {
    inputType() {
      return this.isPassword && !this.showPassword ? 'password' : 'text';
    },
    isPasswordField() {
      return this.isPassword;
    }
  },
  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword;
    }
  }
};
</script>

<style scoped>
.input {
  width: 100%;
  border: 1px solid #61f798;
  padding: 10px 15px;
  margin-top: 15px;
  border-radius: 0.5em;
}
</style>
