import {Body, Controller, Get, Patch, Post, Param} from "@nestjs/common";
import {ApiCreatedResponse, ApiOkResponse, ApiTags} from "@nestjs/swagger";
@ApiTags("workflows")
@Controller("api/workflows")
export class WorkflowsController {
  @Get() @ApiOkResponse({description:"Workflow list"})
  list(){ return []; }
  @Post() @ApiCreatedResponse({description:"Workflow created"})
  create(@Body() body: unknown){ return {id:"poc-workflow"}; }
  @Patch(":id/enabled") update(@Param("id") id:string,@Body() body:{enabled:boolean}){
    return {id,enabled:body.enabled};
  }
}
