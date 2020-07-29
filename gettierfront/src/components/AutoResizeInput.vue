<template>
 
</template>
<script>
export default {
  name: "ResizeByMixin",
  props: ["value"],
 
};
</script>
<style>
.textarea {
  resize: none !important;
  background-color: rgba(0, 0, 0, .05);
  
  border-radius: 25px;
  padding: 10px;
  width: 100%;
  
}
.textarea:focus {
  outline: 0px !important;
  -webkit-appearance: none;
  box-shadow: none !important;
}
.wrapper {
  width: 100%;
  margin-left:5px;
}
</style>
