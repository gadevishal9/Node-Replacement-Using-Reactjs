import React from 'react';
import Heading from '../Heading/Heading'
import Description from '../Description/Description'
import NumberSubmit from '../NumberSubmit/NumberSubmit'
var project_description = "Description of the project";


class Project extends React.Component{
    render(){
      return(
          <div>
              <Heading heading = "Project 1 heading"></Heading>
       <Description details = {project_description}></Description>
        <NumberSubmit></NumberSubmit>
          </div>
       
    //    <ButtonComponent></ButtonComponent>
      );
    }
  }
  export default Project;