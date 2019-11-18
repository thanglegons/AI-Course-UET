# AI-Course-UET
# P1: Search
# P2: Multi-agents

Youtube Link: https://www.youtube.com/watch?v=jB1zN38PAZU&feature=youtu.be
### Question 1:
*Yêu cầu:* Tối ưu hàm ReflexAgent, một game_state có score cao hơn thì tốt hơn

*Cách làm:*

 - Chia một game state thành hai tình huống:
 - Nếu khoảng cách nhỏ nhất của ghost < 3 trả về âm vô cùng
 - Ngược lại: score sẽ được tính theo công thức: 
 $$
 score = - 1000 * numFoodLeft - 50 * minDistanceToFood
 $$
 trong đó: numFoodLeft là số lượng food còn lại, minDistanceToFood là khoảng cách nhỏ nhất của Pacman đến food gần nhất.
  - Với bài này các khoảng cách được tính theo khoảng cách Manhatann
### Question 2:
*Yêu cầu:* Implement Minimax cho Pacman

*Cách làm:*
 - Tạo một hàm đệ quy $$ minimax(depth, gameState, agent) $$
 - trong đó: depth là độ sâu hiện tại của cây minimax, gameState là game state hiện tại, agent là agent đang thực hiện.
 - nếu agent == 0 (agent là Pacman):
 $$ minimax(depth, gameState, agent) = max(minimax(nextDepth, nextGameState, nextAgent))$$
 - Nếu agent != 0 (agent là ghost):
 $$ minimax(depth, gameState, agent) = min(minimax(nextDepth, nextGameState, nextAgent))$$

### Question 3:
*Yêu cầu:* Implement Alpha Beta Pruning cho Pacman

*Cách làm:*
 - Tạo một hàm hai đệ quy $$ pruningMax(depth, gameState, agent, alpha, beta) $$ và $$ pruningMin(depth, gameState, agent, alpha, beta) $$ Trong đó alpha là best score của các nút Max, beta là best score của các nút Min.
 - Với hàm Max: Duyệt các nextGameState, nếu score của nextGameState vượt quá beta, dừng lại (vì nếu duyệt tiếp, kết quả sẽ không bị ảnh hưởng), ngược lại thì cập nhật **alpha = max(alpha, score).**
- Với hàm Min: Duyệt các nextGameState, nếu score của nextGameState nhỏ hơn alpha, dừng lại (vì nếu duyệt tiếp, kết quả sẽ không bị ảnh hưởng), ngược lại thì cập nhật **beta = min(beta, score).**
 
 ### Question 4:
*Yêu cầu:* Implement Expectimax cho Pacman

*Cách làm:*
 - Tương tự như hàm của Minimax nhưng với mỗi nút Min thay vì lấy Min score của các trạng thái game tiếp theo thì sẽ lấy Expected value score của các trạng thái đó (giả sử các ghost sẽ chọn các action theo **uniform** distribution). 

### Question 5:
*Yêu cầu:* Implement evaluation function cho một game state (tương tự với Question 1, score càng cao tức là trạng thái đó càng tốt)

*Cách làm:*
 - Trong 1 game state sẽ có 3 tình huống xảy ra:
 - Một là khoảng cách của Pacman đến ghost < 3 thì trả ra score là âm vô cùng
 - Hai là ít nhất một ghost đang trong trạng thái scared: $$ score = - minDistanceToScaredGhost $$
 - Còn lại: $$score = -numFoodLeft * 1000 - minDistanceToFood * 50 $$
 - Trong đó: minDIstanceToScaredGhost là khoảng cách nhỏ nhất của Pacman đến scared ghost, numFoodLeft là số lượng food còn lại, minDistanceToFood là khoảng cách nhỏ nhất của Pacman đến food gần nhất
 - Khi sử dụng khoảng cách **Manhatann** sẽ xảy ra tình huống khi Pacman, wall và food cùng nằm trên một hàng theo thứ tự đó, khi Pacman di chuyển lên/xuống để đi sang food, khoảng cách Manhatann tăng lên dẫn đến việc Pacman sẽ ưu tiên hành động **Stop**.  
 - Để khắc phục tình huống trên, sử dụng khoảng cách **BFS** sẽ không gặp tình huống đó nhưng trade off lại thời gian tính toán score của mỗi state sẽ tăng lên.


