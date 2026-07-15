import InteractionForm from "../components/InteractionForm";
import ChatBox from "../components/ChatBox";

export default function LogInteraction() {
  return (
    <div className="h-screen w-screen bg-[#f5f6f8] p-6 overflow-hidden">

      <div className="h-full rounded-xl bg-white border border-[#e7e7e7] shadow-[0_8px_30px_rgba(15,23,42,0.05)] flex overflow-hidden">

        {/* Left */}
        <div className="flex-1 overflow-y-auto">
          <div className="max-w-[1080px] mx-auto px-10 py-9">
            <InteractionForm />
          </div>
        </div>

        {/* Right */}
        <div className="w-[400px] border-l border-[#ececec] bg-white shrink-0">
          <ChatBox />
        </div>

      </div>

    </div>
  );
}