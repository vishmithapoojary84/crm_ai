import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  messages: [],
  extractedData: null,
};

const interactionSlice = createSlice({
  name: "interaction",
  initialState,
  reducers: {
    addMessage: (state, action) => {
      state.messages.push(action.payload);
    },
    clearChat: (state) => {
      state.messages = [];
    },
    // Merges previous and current state parameters smoothly to support partial form updates
    setExtractedData: (state, action) => {
      state.extractedData = {
        ...state.extractedData,
        ...action.payload
      };
    },
    clearExtractedData: (state) => {
      state.extractedData = null;
    }
  },
});

export const { addMessage, clearChat, setExtractedData, clearExtractedData } = interactionSlice.actions;
export default interactionSlice.reducer;