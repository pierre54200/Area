import {useCallback} from "react";
import {ReactFlow, Background, Controls, addEdge, useEdgesState, useNodesState} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
const initialNodes=[{id:"trigger",position:{x:0,y:80},data:{label:"Trigger"},type:"input"},
 {id:"condition",position:{x:220,y:80},data:{label:"Condition"}},
 {id:"reaction",position:{x:440,y:80},data:{label:"Reaction"},type:"output"}];
const initialEdges=[{id:"e1",source:"trigger",target:"condition"},{id:"e2",source:"condition",target:"reaction"}];
export default function BuilderWeb(){
 const [nodes,,onNodesChange]=useNodesState(initialNodes);
 const [edges,setEdges,onEdgesChange]=useEdgesState(initialEdges);
 const onConnect=useCallback((connection)=>setEdges((eds)=>addEdge(connection,eds)),[setEdges]);
 return <div style={{height:480}}><ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} onConnect={onConnect}><Background/><Controls/></ReactFlow></div>;
}
