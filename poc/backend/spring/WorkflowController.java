package poc.area;
import java.util.List;
import java.util.Map;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

@RestController
@RequestMapping("/api/workflows")
public class WorkflowController {
  @GetMapping public List<Map<String,Object>> list(){ return List.of(); }
  @PostMapping public ResponseEntity<Map<String,String>> create(@RequestBody Map<String,Object> body){
    return ResponseEntity.status(HttpStatus.CREATED).body(Map.of("id","poc-workflow"));
  }
  @PatchMapping("/{id}/enabled") public Map<String,Object> enabled(@PathVariable String id,@RequestBody Map<String,Boolean> body){
    return Map.of("id",id,"enabled",body.getOrDefault("enabled",false));
  }
}
