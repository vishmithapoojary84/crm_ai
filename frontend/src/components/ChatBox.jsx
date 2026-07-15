import { useState, useRef, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Bot, SendHorizontal } from "lucide-react";
import client from "../api/client";
import {
  addMessage,
  setExtractedData,
} from "../features/interaction/interactionSlice";

export default function ChatBox() {
  const [input, setInput] = useState("");

  const dispatch = useDispatch();

  const messages = useSelector(
    (state) => state.interaction?.messages || []
  );

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const message = input;

    dispatch(
      addMessage({
        role: "user",
        content: message,
      })
    );

    setInput("");

    try {
      const res = await client.post("/chat/", {
        message,
      });

      dispatch(
        addMessage({
          role: "assistant",
          content: res.data.response,
        })
      );

      if (res.data.extracted_data) {
        dispatch(
          setExtractedData(res.data.extracted_data)
        );
      }
    } catch {
      dispatch(
        addMessage({
          role: "assistant",
          content:
            "Unable to connect to AI Assistant.",
        })
      );
    }
  };

  return (
    <div className="flex flex-col h-full bg-white">

      {/* Header */}

      <div className="border-b border-[#ececec] px-7 py-6">

        <div className="flex items-center gap-2">

          <div className="w-8 h-8 rounded-full bg-[#EEF4FF] flex items-center justify-center">

            <Bot
              size={18}
              className="text-[#0052FF]"
            />

          </div>

          <div>

            <h2 className="text-[17px] font-semibold text-[#0052FF]">
              AI Assistant
            </h2>

            <p className="text-[12px] text-[#7c7c7c] mt-0.5">
              Log interaction details here via chat
            </p>

          </div>

        </div>

      </div>

      {/* Messages */}

      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-4">

        <div className="bg-[#E8F9FD] rounded-2xl p-4 text-[13px] leading-6 text-[#374151] border border-[#D6F1F7]">

          Log interaction details here.

          <br />

          Example:

          <br />

          <span className="text-[#0052FF]">

            Met Dr. Smith yesterday, discussed
            Prodo-X efficacy, positive response,
            shared brochure.

          </span>

        </div>

        {messages.map((msg, index) => (

          <div
            key={index}
            className={`flex ${
              msg.role === "user"
                ? "justify-end"
                : "justify-start"
            }`}
          >

            <div
              className={`max-w-[88%] px-4 py-3 text-[13px] leading-6 ${
                msg.role === "user"
                  ? "bg-[#0052FF] text-white rounded-2xl rounded-br-md"
                  : "border border-[#e5e7eb] bg-white text-[#444] rounded-2xl rounded-bl-md"
              }`}
            >
              {msg.content}
            </div>

          </div>

        ))}

        <div ref={messagesEndRef} />

      </div>
          {/* Input */}

      <div className="border-t border-[#ececec] p-6 bg-white">

        <div className="flex items-center gap-3">

          <div className="flex-1 border border-[#d9d9d9] rounded-xl h-[50px] flex items-center px-4 bg-white focus-within:border-[#0052FF] transition-colors">

            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  sendMessage();
                }
              }}
              placeholder="Describe Interaction..."
              className="w-full outline-none text-[13px] text-[#444] placeholder:text-[#9ca3af] bg-transparent"
            />

          </div>

          <button
            onClick={sendMessage}
            disabled={!input.trim()}
            className="w-[62px] h-[50px] rounded-xl bg-[#0052FF] hover:bg-[#0047E6] disabled:bg-[#9bbcff] text-white flex flex-col items-center justify-center transition-all duration-200"
          >

            <SendHorizontal
              size={18}
              strokeWidth={2.3}
            />

            <span className="text-[10px] font-semibold mt-0.5">
              Log
            </span>

          </button>

        </div>

      </div>

    </div>
  );
}