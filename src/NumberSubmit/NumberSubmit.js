import React from 'react';
import { Graph } from 'react-d3-graph';
import axios from "axios";
const final_graph = require('../final_graph.json')
const mst_graph = require('../mst_graph.json')
const initial_graph = require('../initial_graph.json')
console.log(typeof initial_graph);
const myConfig = {
    nodeHighlightBehavior: true,
    node: {
        color: 'lightgreen',
        size: 120,
        highlightStrokeColor: 'blue',
        labelProperty : 'id'
    },
    link: {
        highlightColor: 'lightblue',
        labelProperty : 'label',
        renderLabel: true
    }
};
 
// graph event callbacks


class NumberSubmit  extends  React.Component{
state = {
    'nodes': 0,
    'budget' : 1,
    create_graph : false,
    number: 1,
    answer_graph: final_graph,
    initial_graph : initial_graph,
    mst_graph : mst_graph

}

handleNodesChange = (event) => {
    this.setState({'nodes' : event.target.value});
}
handleBudgetChange = (event) => {
    this.setState({'budget' : event.target.value});
}
handleSubmit = () => {
    
    var data = {
        'budget': this.state.budget,
        'nodes': this.state.nodes
    };
    
    // var data = new FormData();
    // data.append( "json", JSON.stringify( payload ) );
    fetch('http://localhost:5000/',{
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
       body: JSON.stringify(data)
    })
    .then(res=>res.text())
    .then(
        (result) =>{
            
            var result1 = JSON.parse(result);
            console.log(result1['all_graphs'][2]['final_graph']);
            this.setState({initial_graph: JSON.parse(result1['all_graphs'][0]['initial_graph'])});
            this.setState({mst_graph: JSON.parse(result1['all_graphs'][1]['mst_graph'])});
            this.setState({answer_graph: JSON.parse(result1['all_graphs'][2]['final_graph'])});
        }
    )
    // console.log(this.state.answer_graph);
    this.setState({create_graph: true});

}
render(){
    let graph_content;
    if(this.state.create_graph){
        graph_content = <div>
            <h1>
                This is Fully Completed  Graph with {this.state.nodes} nodes and Budget is : {this.state.budget}
            </h1>
     <Graph
    id="graph-id" // id is mandatory, if no id is defined rd3g will throw an error
    data={this.state.initial_graph}
    config={myConfig}
    />
    <h1>
        This is Minimum Spanning Graph for above graph
    </h1>
    <Graph
    id="graph-id" // id is mandatory, if no id is defined rd3g will throw an error
    data={this.state.mst_graph}
    config={myConfig}
    /> 
    <h1>
        This is the Final Graph
    </h1>
    <Graph
    id="graph-id" // id is mandatory, if no id is defined rd3g will throw an error
    data={this.state.answer_graph}
    config={myConfig}
    />
     </div>
    }
    else{
        graph_content = null;
    }
    return(
        <div>
            
        Number of terminal nodes: 
          <input type="text" nodes={this.state.nodes} onChange={this.handleNodesChange} />
          <br></br>
          Enter the Budget:
          <input type="text" nodes={this.state.budget} onChange={this.handleBudgetChange} />
            <br></br>
            <button onClick = {this.handleSubmit}> create graphs </button>
        
            {graph_content}
            <p>{this.state.number}</p>
        </div>
       
    );
}
}
export default NumberSubmit;