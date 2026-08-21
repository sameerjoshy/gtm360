import { Route, Routes } from "react-router-dom";

import { Layout } from "./components/Layout";
import { BriefingView } from "./components/views/BriefingView";
import { ContentView } from "./components/views/ContentView";
import { HygieneView } from "./components/views/HygieneView";
import { HomeView } from "./components/views/HomeView";
import { OutboundView } from "./components/views/OutboundView";
import { ResearcherView } from "./components/views/ResearcherView";
import { SalesView } from "./components/views/SalesView";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<HomeView />} />
        <Route path="/researcher" element={<ResearcherView />} />
        <Route path="/hygiene" element={<HygieneView />} />
        <Route path="/sales" element={<SalesView />} />
        <Route path="/content" element={<ContentView />} />
        <Route path="/briefing" element={<BriefingView />} />
        <Route path="/outbound" element={<OutboundView />} />
      </Route>
    </Routes>
  );
}