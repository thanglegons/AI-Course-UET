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
 <img src="https://tex.s2cms.ru/svg/%0A%20score%20%3D%20-%201000%20*%20numFoodLeft%20-%2050%20*%20minDistanceToFood%0A%20" alt="
 score = - 1000 * numFoodLeft - 50 * minDistanceToFood
 " />
 trong đó: numFoodLeft là số lượng food còn lại, minDistanceToFood là khoảng cách nhỏ nhất của Pacman đến food gần nhất.
  - Với bài này các khoảng cách được tính theo khoảng cách Manhatann
### Question 2:
*Yêu cầu:* Implement Minimax cho Pacman

*Cách làm:*
 - Tạo một hàm đệ quy <img src="https://tex.s2cms.ru/svg/%20minimax(depth%2C%20gameState%2C%20agent)%20" alt=" minimax(depth, gameState, agent) " />
 - trong đó: depth là độ sâu hiện tại của cây minimax, gameState là game state hiện tại, agent là agent đang thực hiện.
 - nếu agent == 0 (agent là Pacman):
 <img src="https://tex.s2cms.ru/svg/%20minimax(depth%2C%20gameState%2C%20agent)%20%3D%20max(minimax(nextDepth%2C%20nextGameState%2C%20nextAgent))" alt=" minimax(depth, gameState, agent) = max(minimax(nextDepth, nextGameState, nextAgent))" />
 - Nếu agent != 0 (agent là ghost):
 <img src="https://tex.s2cms.ru/svg/%20minimax(depth%2C%20gameState%2C%20agent)%20%3D%20min(minimax(nextDepth%2C%20nextGameState%2C%20nextAgent))" alt=" minimax(depth, gameState, agent) = min(minimax(nextDepth, nextGameState, nextAgent))" />

### Question 3:
*Yêu cầu:* Implement Alpha Beta Pruning cho Pacman

*Cách làm:*
 - Tạo một hàm hai đệ quy <img src="https://tex.s2cms.ru/svg/%20pruningMax(depth%2C%20gameState%2C%20agent%2C%20alpha%2C%20beta)%20" alt=" pruningMax(depth, gameState, agent, alpha, beta) " /> và <img src="https://tex.s2cms.ru/svg/%20pruningMin(depth%2C%20gameState%2C%20agent%2C%20alpha%2C%20beta)%20" alt=" pruningMin(depth, gameState, agent, alpha, beta) " /> Trong đó alpha là best score của các nút Max, beta là best score của các nút Min.
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
 - Hai là ít nhất một ghost đang trong trạng thái scared: <img src="https://tex.s2cms.ru/svg/%20score%20%3D%20-%20minDistanceToScaredGhost%20" alt=" score = - minDistanceToScaredGhost " />
 - Còn lại: <img src="https://tex.s2cms.ru/svg/score%20%3D%20-numFoodLeft%20*%201000%20-%20minDistanceToFood%20*%2050%20" alt="score = -numFoodLeft * 1000 - minDistanceToFood * 50 " />
 - Trong đó: minDIstanceToScaredGhost là khoảng cách nhỏ nhất của Pacman đến scared ghost, numFoodLeft là số lượng food còn lại, minDistanceToFood là khoảng cách nhỏ nhất của Pacman đến food gần nhất
 - Khi sử dụng khoảng cách **Manhatann** sẽ xảy ra tình huống khi Pacman, wall và food cùng nằm trên một hàng theo thứ tự đó, khi Pacman di chuyển lên/xuống để đi sang food, khoảng cách Manhatann tăng lên dẫn đến việc Pacman sẽ ưu tiên hành động **Stop**.  
 - Để khắc phục tình huống trên, sử dụng khoảng cách **BFS** sẽ không gặp tình huống đó nhưng trade off lại thời gian tính toán score của mỗi state sẽ tăng lên.

# P5: Classification

Youtube Link: https://www.youtube.com/watch?v=jB1zN38PAZU&feature=youtu.be
### Question 1:
*Yêu cầu:* Implement training Perceptron

*Cách làm:*

- Với mỗi training data (feature: f, correct label: y)
- Tính y' là nhãn dự đoán bằng cách tính score của f với từng label rồi chọn label có score lớn nhất
- Nếu <img src="https://tex.s2cms.ru/svg/%20y'%20%3D%3D%20y%20" alt=" y' == y " /> thì không làm gì cả
- Ngược lại cập nhật lại weight của label y và y'
### Question 2:
*Yêu cầu:* Perceptron Analysis

*Cách làm:*
- Visualize top 100 features có trọng số lớn nhất

### Question 3:
*Yêu cầu:* Implement training MIRA

*Cách làm:*
- Làm tương tự với Perceptron
- Khi cập nhật weight, chọn tham số <img src="https://tex.s2cms.ru/svg/%20%5Ctau%20" alt=" \tau " /> thoả mãn

<img src="https://tex.s2cms.ru/svg/%20%5Cmin%5Climits_%7Bw'%7D%20%5Cfrac%7B1%7D%7B2%7D%20%5Csum%5Climits_%7Bc%7D%20%7C%7C(w')%5Ec%20-%20w%5Ec%20%7C%7C_2%5E2%20" alt=" \min\limits_{w'} \frac{1}{2} \sum\limits_{c} ||(w')^c - w^c ||_2^2 " />
- Sau một vài biến đổi, ta có:

<img src="https://tex.s2cms.ru/svg/%20%5Ctau%20%3D%20%5Cmin%20(%20C%2C%20%5Cfrac%7B(w%5E%7By'%7D%20-%20w%5Ey)f%20%2B%201%7D%7B2%7C%7Cf%7C%7C_2%5E2%7D%20)%20" alt=" \tau = \min ( C, \frac{(w^{y'} - w^y)f + 1}{2||f||_2^2} ) " />
- Với C là hằng số dương (fine-tuned parameter bằng Validation Data)

### Question 4:
*Yêu cầu:* Thiết kế feature cho bài toán Digit Recognition

*Cách làm:*
- Chọn thêm 4 features:
- Đếm số lượng thành phần liên thông chỉ gồm các pixel có giá trị 0 <img src="https://tex.s2cms.ru/svg/%20(%3E%201%2C%20%3E%203%2C%20%3E%205)%20" alt=" (&gt; 1, &gt; 3, &gt; 5) " />
- Tỉ lệ các pixel có giá trị 1 nằm nữa trên của ảnh <img src="https://tex.s2cms.ru/svg/%20(%3E%2050%20%5C%25%20)%20" alt=" (&gt; 50 \% ) " />
### Question 5:
*Yêu cầu:* Implement Perceptron cho Pacman

*Cách làm:*
 
- Với từng action và state, công thức score:

<img src="https://tex.s2cms.ru/svg/%20score(s%2C%20%5Ctext%7Ba%7D)%20%3D%20w*f(s%2Ca)%20" alt=" score(s, \text{a}) = w*f(s,a) " />
- predicted action được tính theo công thức:

<img src="https://tex.s2cms.ru/svg/%20a'%20%3D%20arg%20%5Cmax%5Climits_%7Ba''%7D%20score%20(s%2Ca'')%20" alt=" a' = arg \max\limits_{a''} score (s,a'') " />
- Weight của các label được dùng chung và được update theo công thức:

<img src="https://tex.s2cms.ru/svg/%20w%3D%20w%2B%20f(s%2Ca)%20" alt=" w= w+ f(s,a) " />

<img src="https://tex.s2cms.ru/svg/%20w%3D%20w-%20f(s%2Ca')%20" alt=" w= w- f(s,a') " />

### Question 6:
*Yêu cầu:* Thiết kế feature cho Pacman

*Cách làm:*
 
- Chọn các feature:

- Min distance đến các ghosts
- Min distance đến các capsules
- 3 Min distances đến các foods