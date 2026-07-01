# Bellmanford.c

`
    
    
    
    /*********************************
    FILE: parser
    This program takes as input a file where the first row is the number of vertices, the index of the starting vertex, and the index of the finish vertex.  The next N rows are in the format of the vertex index (1, 2, 3, 4... N) followed by N doubles (tab delimited) that represent the weights from the from the vertex represented by the row to the vertex represented by the column.  If there is no connection between the two vertices, it is represented by "inf" which is float type macro defined in math.h that represents infinity essentially.  The program recognizes this symbol and treats as though there were no edge.
    
    When all is said and done, each process will be responsible for edge_num edges.  Each process will be left with an array called reduced_edges where entry 2k is the leading node of the kth edge for that task, and the 2k+1 entry is the ending node of that edge.  Similarly each task will have an array called reduced_weights where the kth entry is the weight associated to the kth edge of that task.
    *********************************/
    
    #include <mpi.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>
    #define MASTER 0
    
    int printintarray(int *our_array, int array_size) {
      int i;
      printf("Array: ");
      for(i=0;i<array_size;i++) {
        printf("%d,", our_array[i]);
      }
      printf("\n");
      return(0);
    } 
    
    
    int printdoublearray(double *our_array, int array_size) {
      int i;
      printf("Array: ");
      for(i=0;i<array_size;i++) {
        printf("%f,", our_array[i]);
      }
      printf("\n");
      return(0);
    } 
    
    int old_whichtask(int node, int chunk, int leftover_nodes) {
      int tasknum;
      node -= 1;
      tasknum = node / chunk;
      if ((tasknum != 0) && (tasknum-1 < leftover_nodes) && (node % chunk == 0)) {
        tasknum--; // then this node belongs to the lower task number
      }
      return tasknum;
    }
    int whichtask(int node, int chunk, int leftover) {
      node -= 1;
      int x = node/chunk;
      if (x > leftover)
        x = leftover;
      return((node-x)/chunk);
    }
    
    int first_node_in_task (int task, int chunk, int leftover) {
      int x = task; // x accounts for the stagger caused by the leftovers
      if (x > leftover) 
        x = leftover;
      return(chunk*task + x);
    }
    
    int quicksort_edges(int *edge_array, double *weight_array, int edgearray_len, int weightarray_len, int basis) {
      // sorts edges by increasing destination indeces if basis == 1, 
      // if basis == 0, sorts by src
      int pivot[2];
      double pivotweight;
      int pivot_loc = weightarray_len/2; // to ensure its even
      int edge_pivot_loc = pivot_loc*2;
      int i, greater_index = 0, less_index = 0;
      if (weightarray_len <= 1) { // an array of length 0 or 1 is already sorted
        return(0);
      }
      pivot[0] = edge_array[edge_pivot_loc]; // choose a pivot halfway in
      pivot[1] = edge_array[edge_pivot_loc+1];
      pivotweight = weight_array[pivot_loc]; // choose the pivot weight
      int less_len = (weightarray_len/2);
      int greater_len = weightarray_len - less_len;
      int less[weightarray_len*2]; // contains edges
      //int *less;
      //less = malloc(weightarray_len * 2 * sizeof(int));
      double lessweights[weightarray_len];
      int greater[weightarray_len*2];
      double greaterweights[weightarray_len];
      int memsize;
      for (i=0; i<weightarray_len; i++) {
        if (i == pivot_loc) {
          continue;
        } else if (edge_array[2*i + basis] <= pivot[basis]) { // comparing the pivot dest node to every other dest node
          // then append x to less
          less[less_index*2] = edge_array[i*2];
          less[less_index*2 + 1] = edge_array[i*2+1];
          lessweights[less_index] = weight_array[i];
          less_index++; 
        } else {
          // then append x to greater 
          greater[greater_index*2] = edge_array[i*2];
          greater[greater_index*2+1] = edge_array[i*2+1];
          greaterweights[greater_index] = weight_array[i];
          greater_index++;
        }
      }
      quicksort_edges(&less[0], &lessweights[0], less_index*2, less_index, basis);
      quicksort_edges(&greater[0], &greaterweights[0], greater_index*2, greater_index, basis);
      // now copy the memory to the corresponding locations
      memsize = less_index*sizeof(int);
      memcpy(edge_array, less, memsize*2);
      memsize = less_index*sizeof(double);
      memcpy(&weight_array[0], lessweights, memsize);
      edge_array[less_index*2] = pivot[0];  // copy the pivot to the end of the less array
      edge_array[less_index*2+1] = pivot[1];
      weight_array[less_index] = pivotweight;
      memsize = greater_index*sizeof(int);
      memcpy(edge_array+(less_index+1)*2, greater, memsize*2);
      memsize = greater_index*sizeof(double);
      memcpy(weight_array+less_index+1, greaterweights, memsize);
      return(0);
    }
    
    int send_noedges_to_missed_tasks(int taskid, int nexttask, int curtask) {
      int i;
      int zero = 0;
      MPI_Request request;
      if (nexttask - curtask <= 1) { // the task numbers are adjacent; we don't need to send anything to anyone
        return(0);
      } else { // then we need to send zero edge_numbers to every task in between
        for (i=1; i<(nexttask-curtask); i++) {
          if (curtask+i != taskid) {
            //printf("task: %d sending zero edges to task: %d\n", taskid, curtask+i);
            MPI_Isend(&zero, 1, MPI_INT, (curtask + i), 0, MPI_COMM_WORLD, &request);
          }
        }
      }
    }
    
    int fill_task_array(int *arraystart, int fillvalue, int nexttask, int curtask) {
      int i;
      if (nexttask - curtask <= 1) { // adjacent
        return(0);
      } else {
        for (i=1; i<(nexttask-curtask); i++) {
          arraystart[i+curtask] = fillvalue;
        }
      }
    }
    
    int main (int argc, char* argv[]) 
    {
      int N, taskid, i, f, j, k, p, tag1=1, tag2=2, tag3=3, tag4=4, holder,numprocs, start_vertex, finish_vertex, vpn, leftover;
      int destination, source, vpn2;
    double weight;
     int current_vertex, edge_num, edge_num2;
    double starttime, endtime;
    int counter=0;
    int memsize;
    //double INF = infinity();
    starttime = MPI_Wtime();
    
    MPI_Init(&argc, &argv); //starting MPI
    MPI_Comm_size(MPI_COMM_WORLD, &numprocs); // Get the number of tasks
    MPI_Comm_rank(MPI_COMM_WORLD, &taskid); // identify this task
     MPI_Status status;
     MPI_Request request;
     MPI_Status statusarray[numprocs*2];
     MPI_Request requestarray[numprocs*2];
     //These next three broadcasts make sure that every process knows the value of N, and which are the starting and finishing vertices
     // broadcasting N, start_vertex, finish_vertex
     if(taskid == 0){
       scanf("%d", &N);//Number of vertices
       scanf("%d", &start_vertex);//starting vertex
       scanf("%d", &finish_vertex);//finish vertex
    
       holder = MPI_Bcast(&N, 1, MPI_INT, 0, MPI_COMM_WORLD);
       holder = MPI_Bcast(&start_vertex, 1, MPI_INT, 0, MPI_COMM_WORLD);
       holder = MPI_Bcast(&finish_vertex, 1, MPI_INT, 0, MPI_COMM_WORLD);
     
     }else{
       holder = MPI_Bcast(&N, 1, MPI_INT, 0, MPI_COMM_WORLD);
       holder = MPI_Bcast(&start_vertex, 1, MPI_INT, 0, MPI_COMM_WORLD);
       holder = MPI_Bcast(&finish_vertex, 1, MPI_INT, 0, MPI_COMM_WORLD);
     }
    
    vpn = N / numprocs;
    leftover = N % numprocs;
    
    //  printf("task %d leftover: %d, vpn2: %d\n",taskid,  leftover, vpn2);
     
     int num_out_edges_total=0; // the total number of outgoing edges in this task
     int *out_edges; 
     double *out_weights;
    
    if(taskid == 0){
       int temp_edges[2*N*(1+vpn)];
       double temp_weights[N*(1+vpn)];
       //first, the master task reads in however many vertices it is responsible for and assigns it to its local array of weights and edges
       edge_num = 0;
       if(leftover > 0){
         vpn2 = vpn + 1;
       }else{
         vpn2 = vpn;
       }
       // Read the file and assign edge variables FOR TASK 0
       for(i = 0; i < vpn2; i++){
         scanf("%d", &current_vertex);
         for(j = 0; j < N; j++){
           scanf("%lf", &weight);
           if(isfinite(weight) != 0){
             temp_weights[edge_num] = weight;
             temp_edges[2*edge_num] = current_vertex;
             temp_edges[(2*edge_num) + 1] = j + 1;
             edge_num++;
           }
         }
       }
       num_out_edges_total = edge_num; // assign the total number of outgoing edges for this task
       // assign the edges for task 0
       // NOTE: should first dynamically allocate appropriate memory size
       out_edges = malloc(num_out_edges_total * 2 * sizeof(int));
       out_weights = malloc(num_out_edges_total * sizeof(double)); 
       for(i = 0; i< num_out_edges_total; i++){
         out_weights[i] = temp_weights[i];
         out_edges[2*i] = temp_edges[2*i];
         out_edges[(2*i) + 1] = temp_edges[(2*i)+1];
       }
       //master task repeats this process for each other task, stores the values in temp_edges and temp_weights then sends it to the corresponding task
       for(k = 1; k < numprocs; k++){ // loop through all other processors
         edge_num = 0;
         
         if(k < leftover){
           vpn2 = vpn + 1;
         }else{
           vpn2 = vpn;
         }
         
         for(i = 0; i < vpn2; i++){ // for every other vector in this node
           scanf("%d", &current_vertex);
           for(j = 0; j < N; j++){
             scanf("%lf", &weight);
             if(isfinite(weight) != 0){ // if there's an edge here
               temp_weights[edge_num] = weight;
               temp_edges[2*edge_num] = current_vertex; // then add an edge
               temp_edges[(2*edge_num) + 1] = j + 1;
               edge_num++;
             }
           }
         }
    
         MPI_Isend(&edge_num, 1, MPI_INT, k, tag1, MPI_COMM_WORLD, &request); // send the number of edges to this node
         if (edge_num > 0) { // if there are any outgoing edges to these nodes, then send them
           //printf("Master task sending %d edges to task %d, a total of %d units of memory\n", edge_num, k, edge_num*2*sizeof(int));
           MPI_Send(&temp_edges, 2*edge_num, MPI_INT,    k, tag2, MPI_COMM_WORLD);
           MPI_Send(&temp_weights, edge_num, MPI_DOUBLE, k, tag3, MPI_COMM_WORLD);
           //printf("Master task temp_edges index:");
           //printintarray(&temp_edges[0], 2*edge_num);
         }
       }
       //the tasks receive the values and store them in their local arrays of edges and weights
     }else{
       MPI_Recv(&num_out_edges_total, 1, MPI_INT, 0, tag1, MPI_COMM_WORLD, &status); // NOTE: malloc the needed size
       //holder = MPI_Wait(&request, &status);
       if (num_out_edges_total > 0) { // if this task has any edges going into it then allocate some memory and recieve those edges
         out_edges   = malloc(num_out_edges_total * sizeof(int) * 2);
         out_weights = malloc(num_out_edges_total * sizeof(double));
         //printf("task %d allocated: %d memory for edges. %d memory for weights\n", taskid, num_out_edges_total*2*sizeof(int), num_out_edges_total*sizeof(double));
         MPI_Recv(out_edges, 2*num_out_edges_total, MPI_INT,    0, tag2, MPI_COMM_WORLD, &status);
         MPI_Recv(out_weights, num_out_edges_total, MPI_DOUBLE, 0, tag3, MPI_COMM_WORLD, &status);
         //printf("task %d out_edge array from index 1000 to 1025:", taskid);
         //printintarray(&out_edges[0], num_out_edges_total*2);
       }
    }
    // make sure that the node knows how many vertices per node we should have
    if (taskid < leftover)
      vpn2 = vpn + 1;
    else
      vpn2 = vpn;
    
    //printf("task %d: num_outgoing_edges_total: %d\n out_edges:", taskid, num_out_edges_total);
    //printintarray(out_edges,2*num_out_edges_total);
    //printdoublearray(out_weights, num_out_edges_total);
    
    
    int curtask;
    int nexttask;
    int srcnode;
    int destnode;
    int num_out_edges_cumulative[numprocs+1];
    int num_out_edges_blocked[numprocs+1];
    int counted_out_edges_num_tasks = 0; // the number of tasks we have outward edges going to
    int counted_out_edges_cumulative[numprocs+1]; // only contains entries for tasks that we have an edge to
    int counted_out_edges_blocked[numprocs+1];
    int counted_out_edges_tasks[numprocs+1];
    int num_out_tasks_total=0;
    int num_out_edges_not_to_self=0;
    //int old_destnode=-1;
    int edges_for_this_task=0;
    //int checkpoint = 0;
    //int self_subtract_factor=0; // we need to subtract this number so that the index of ourselves is not counted
    int num_edges_to_myself = 0;
    int *edges_to_myself;
    double *edges_to_myself_weights;
    //int num_outgoing_nodes=0;
    //int num_outgoing_tasks=0;
    //int outgoing_num_edges[numprocs];
    //int outgoing_tasks[numprocs];
    //int cumulative_outgoing_edges[numprocs];
    //int outgoing_nodes_indeces=0
    //int num_src_nodes_counted=0;
    //int src_edges[edge_num];
    //memcpy(&src_edges, edges, 2*edge_num*sizeof(int));
    
    quicksort_edges(out_edges, out_weights, 2*num_out_edges_total, num_out_edges_total, 1); // sort the edges by destination node
    
    curtask = -1;
    nexttask = whichtask(out_edges[1], vpn, leftover); // this is the first task in the out_edge array
    fill_task_array(&num_out_edges_blocked[0],    0, nexttask, curtask); // make sure that we fill the num_out_edges_blocked array with zeros up to the first edge
    fill_task_array(&num_out_edges_cumulative[0], 0, nexttask, curtask); // make sure that we fill the num_out_edges_cumulative array with zeros up to the first edge
    send_noedges_to_missed_tasks(taskid,nexttask,curtask); // we must send every task not recieving edges zeros up to the first edge
    curtask = nexttask;
    counter=0;
    num_out_edges_cumulative[curtask] = 0;
    num_out_edges_blocked[curtask] = 0;
    counted_out_edges_cumulative[0] = 0;
    counted_out_edges_blocked[0] = 0;
    //printf("task %d mark0\n", taskid);
    for (i=0;i<=num_out_edges_total;i++) { // for each member of the edge matrix, and an extra just to be sure it's sent off
      if (i < num_out_edges_total) { // this is just to make sure that we are still in the edges, as soon as this goes over, then its time to send off the last task
        srcnode = out_edges[i*2];
        destnode = out_edges[(i*2)+1];
        nexttask = whichtask(destnode, vpn, leftover);
      } else { // then we have only to send the last edges to the last task
        nexttask = numprocs; // set this just to fill in the last task with info it will need
      }
      if (num_out_edges_total == 0) {
        curtask = numprocs;
        nexttask = numprocs;
      }
      //printf("task %d: num_out_edges_total=%d, curtask=%d, nexttask=%d, destnode=%d, i=%d\n", taskid, num_out_edges_total, curtask, nexttask, destnode, i);
      //printf("mark1 iteration: %d out of %d\n", i, num_out_edges_total);
      if (nexttask > curtask) { // then we've moved on to a new task
        edges_for_this_task = num_out_edges_blocked[curtask];
        //printf("task %d sending info to task %d\n", taskid, curtask);
        if (curtask != taskid) { // make sure that next node is not ourself, we don't want to MPI_Send to ourself
          //printf("task %d sending %d edges_for_this_task to task %d.\n", taskid, edges_for_this_task, curtask);
          //printf("task %d mark2 on edge %d-%d\n", taskid, srcnode, destnode);
          MPI_Isend(&edges_for_this_task, 1, MPI_INT, curtask, 0, MPI_COMM_WORLD, &request);
          if (edges_for_this_task > 0) {
            //printf("Task %d sending %d edges to task %d starting at edges index %d\nThis is what is being sent:", taskid, edges_for_this_task, curtask, num_out_edges_cumulative[curtask]);
            //printintarray(&out_edges[num_out_edges_cumulative[curtask]*2], edges_for_this_task*2);
            //printdoublearray(&out_weights[num_out_edges_cumulative[curtask]], edges_for_this_task);
            MPI_Isend(&out_edges[num_out_edges_cumulative[curtask]*2], edges_for_this_task*2,  MPI_INT, curtask, tag1, MPI_COMM_WORLD, &request);
            MPI_Isend(&out_weights[num_out_edges_cumulative[curtask]], edges_for_this_task, MPI_DOUBLE, curtask, tag2, MPI_COMM_WORLD, &request);
            //num_out_tasks_total++;
            counted_out_edges_cumulative[counter] = num_out_edges_cumulative[curtask]; // only contains entries for tasks that we have an edge to
            counted_out_edges_blocked[counter] = edges_for_this_task; // ditto
            counted_out_edges_tasks[counter] = curtask;
            num_out_edges_not_to_self += edges_for_this_task;
            counter++;
          } 
        } else { // Then all these edges are to myself
          //printf("task %d number of edges going to myself: %d\n", taskid, edges_for_this_task);
          //self_subtract_factor = edges_for_this_task;
          num_edges_to_myself = edges_for_this_task; // the number of edges to nodes within myself
          edges_to_myself = malloc(num_edges_to_myself * 2 * sizeof(int));
          edges_to_myself_weights = malloc(num_edges_to_myself * sizeof(double));
          memsize = num_edges_to_myself * sizeof(int);
          memcpy(edges_to_myself,         &out_edges[num_out_edges_cumulative[curtask]*2], memsize * 2);
          memsize = num_edges_to_myself * sizeof(double);
          memcpy(edges_to_myself_weights, &out_weights[num_out_edges_cumulative[curtask]], memsize);
        }
        //printf("task %d mark3\n", taskid);
        //printf("task %d filling missing values between task %d and task %d\n", taskid, curtask, nexttask);
        send_noedges_to_missed_tasks(taskid,nexttask,curtask); // make sure we fill in those other tasks between the last task and the one coming up
        fill_task_array(&num_out_edges_blocked[curtask], 0, nexttask, curtask);
        fill_task_array(&num_out_edges_cumulative[curtask], num_out_edges_cumulative[curtask], nexttask, curtask);
        /*if (taskid == 1)
          printf("num_out_edges_cumulative[%d] (%d) = num_out_edges_cumulative[%d] (%d) + edges_for_this_task(%d);\n", nexttask, num_out_edges_cumulative[curtask] + edges_for_this_task, curtask, num_out_edges_cumulative[curtask], edges_for_this_task);
        */
        num_out_edges_cumulative[nexttask] = num_out_edges_cumulative[curtask] + edges_for_this_task;
        num_out_edges_blocked[nexttask] = 0;
        edges_for_this_task = 0;
        curtask = nexttask;
      }
      num_out_edges_blocked[curtask]++;
    }
    //printf("task %d mark 10\n", taskid);
    counted_out_edges_num_tasks = counter;
    /*
    printf("task %d counted_out_edges_tasks: %d\n", taskid, counted_out_edges_num_tasks);
    printf("task %d counted_out_edges_blocked:", taskid);
    printintarray(&counted_out_edges_blocked[0], counted_out_edges_num_tasks);
    printf("task %d counted_out_edges_cumulative:", taskid);
    printintarray(&counted_out_edges_cumulative[0], counted_out_edges_num_tasks);
    printf("task %d num_out_edges_blocked:", taskid);
    printintarray(&num_out_edges_blocked[0], numprocs);
    printf("task %d num_out_edges_cumulative:", taskid);
    printintarray(&num_out_edges_cumulative[0], numprocs);
    */
    //printf("task %d outgoing_num_edges:", taskid);
    //printintarray(&outgoing_num_edges, counter);
    //printf("task: %d Mark5\n", taskid);
    
    
    //fill_task_array(&outgoing_num_edges[curtask], 0, numprocs, curtask);
    //printf("task %d num_out_edges_not_to_self: %d\n", taskid, num_out_edges_not_to_self);
    counter = 0;
    int num_in_edges_total=0;
    int num_in_edges_cumulative[numprocs+1];
    int num_in_edges_blocked[numprocs+1];
    int counted_in_edges_num_tasks = 0; // the number of tasks we have outward edges going to
    int counted_in_edges_cumulative[numprocs+1]; // only contains entries for tasks that we have an edge to
    int counted_in_edges_blocked[numprocs+1];
    int counted_in_edges_tasks[numprocs+1];
    //int incoming_num_edges[numprocs]; // create a list containing the number of incoming edges from every other task
    //int num_incoming_tasks=0;
    //int incoming_nodes[numprocs];
    //int *incoming_tasks;
    //int incoming_nodes_indeces[numprocs];
    //double *incoming_nodes_values;
    //int cumulative_edges[numprocs];
    //int cumulative_nodes[numprocs];
    int *in_edges;
    double *in_weights;
    
    num_in_edges_cumulative[0] = 0;
    counted_in_edges_cumulative[0] = 0;
    //cumulative_nodes[0] = 0;
    //requestarray = malloc(numprocs * sizeof(*requestarray));
    //incoming_num_edges[taskid] = 0; // no nodes will be coming in from ourselves
    
    for (i=0; i<numprocs; i++) {
      if (i == taskid) {
        num_in_edges_blocked[i] = 0; //num_edges_to_myself;
        num_in_edges_cumulative[i+1] = num_in_edges_cumulative[i]; //+ num_edges_to_myself;
        continue;
      } else {
      //printf("task %d waiting to recieve from task %d.\n", taskid, i);
      //
        MPI_Recv(&num_in_edges_blocked[i],1,MPI_INT, i, 0, MPI_COMM_WORLD, &status); // NOTE: come back to this later
        num_in_edges_cumulative[i+1] = num_in_edges_cumulative[i] + num_in_edges_blocked[i];
      
        if (num_in_edges_blocked[i] != 0) {
          counted_in_edges_num_tasks++;
          counted_in_edges_cumulative[counter]=num_in_edges_cumulative[i];
          counted_in_edges_blocked[counter] = num_in_edges_blocked[i];
          counted_in_edges_tasks[counter] = i;
          counter++;
        }
      }
      //printf("task %d recieved %d incoming nodes from task %d\n", taskid, num_in_edges_blocked[i], i);
    }
    //printf("task %d num_in_edges_tasks[i] = \n", taskid, counted_in_edges_tasks[i]);
    //printintarray(&counted_in_edges_cumulative[0], counted_in_edges_num_tasks);
    num_in_edges_total = num_in_edges_cumulative[i];
    //printf("task %d num_in_edges_total: %d", taskid, num_in_edges_total);
    //printintarray(&num_in_edges_cumulative[0], numprocs+1);
    in_edges =   malloc(num_in_edges_total * 2 * sizeof(int)); // given the total number of edges coming in, malloc enough space to hold all the edges,
    in_weights = malloc(num_in_edges_total * sizeof(double)); // malloc enough space to hold all the edge weights
    /*
    int index=0;
    //printf("task %d: num_incoming_tasks: %d\n", taskid, num_incoming_tasks);
    //MPI_Wait(&requestarray[numprocs-1], &statusarray);
    //MPI_Waitall(numprocs-1,requestarray,statusarray);
    */
    //memsize = num_edges_to_myself * sizeof(int);
    //memcpy(&in_edges[num_in_edges_cumulative[taskid]*2], edges_to_myself, memsize * 2);
    //memsize = num_edges_to_myself * sizeof(double);
    //memcpy(&in_weights[num_in_edges_cumulative[taskid]], edges_to_myself_weights, memsize);
    
    for(i=0; i<counted_in_edges_num_tasks; i++) { // for processing each incoming edge
      int index = counted_in_edges_tasks[i];
      //if (num_in_edges
      //printf("task %d now recieving edges from task %d\n", taskid, index);
      if (index == taskid) {
        requestarray[i] = MPI_SUCCESS;
        requestarray[i+numprocs] = MPI_SUCCESS;
      } else {
        MPI_Irecv(&in_edges[counted_in_edges_cumulative[i]*2], counted_in_edges_blocked[i]*2,  MPI_INT, index, tag1, MPI_COMM_WORLD, &requestarray[i]);
        MPI_Irecv(&in_weights[counted_in_edges_cumulative[i]],  counted_in_edges_blocked[i], MPI_DOUBLE, index, tag2, MPI_COMM_WORLD, &requestarray[i+numprocs]);
        //counter++;
      }
    }
    //printf("task %d Mark9\n", taskid);
    MPI_Waitall(counted_in_edges_num_tasks, &requestarray[0], &statusarray[0]);
    MPI_Waitall(counted_in_edges_num_tasks, &requestarray[numprocs], &statusarray[numprocs]);
    //printf("task %d in_edges:", taskid);
    //printintarray(&in_edges[0], num_in_edges_total*2);
    //printf("task %d in_weights:", taskid);
    //printdoublearray(&in_weights[0], num_in_edges_total);
    
    endtime = MPI_Wtime();
    if (taskid == 0)
      printf("initialization time: %f\n", endtime-starttime);
    starttime = MPI_Wtime();
    
    //printf("task %d Mark10\n", taskid);
    // at this point, the graph is initialized, and all that is left is to process it
    double M[vpn2]; // each node in this task has its own best score
    double newM[vpn2];
    int P[vpn2]; // the pointer array, points to the previous best node, whether in this task or not
    double edge_dest_values[num_in_edges_total]; // temporary solution, send the value of all edges' source node
    int task_index_offset; // the offset for finding the indeces within our task
    int srcMindex;
    int destMindex;
    double curscore;
    double otherscore;
    int indexoffset=0;
    double edgeweight=0.0; // temporarily store the weight of a particular edge
    //int num_incoming_edges = cumulative_edges[numprocs-1];
    int nothing_better=1; // keeps track of whether anything better was ever found in this task
    int nothing_better_reduced=0;
    int *nothing_better_array; // in task 0, this array keeps track of when the graph has completed its refinement
    int index;
    int ontask;
    int size;
    double best_path_length=0.0;
    //double *incoming_edge_values;  
    //incoming_edge_values = malloc(edge_num * sizeof(double));
    double *out_edge_values;
    out_edge_values = malloc(num_out_edges_total * sizeof(double)); // this is a temporary solution
    
    indexoffset = first_node_in_task(taskid, vpn, leftover)+1;
    
    task_index_offset = first_node_in_task(taskid, vpn, leftover)+1; // how much do we need to offset the index by
    for (i=0; i<vpn2; i++) { // fill the M and P arrays 
      //printf("In node %d, vpn2=%d, finish_vertex=%d, i=%d\n", taskid, vpn2, finish_vertex, i);
      if ((i+task_index_offset) != finish_vertex) { // if this is not the finish vertex, then the best way to the finish vertex in 0 steps is impossible
        M[i] = HUGE_VAL;
        newM[i] = HUGE_VAL;
      } else {
        //printf("finish_vertex is in node %d\n", taskid);
        M[i] = 0.0; // only the finish vertex itself can get to the finish vertex in 0 steps
        newM[i] = 0.0;
      }
      P[i] = indexoffset + i;
    }
    
    //printf("task %d P ", taskid);
    //printintarray(&P[0],vpn2);
    
    
    //printf("task: %d incoming edges:", taskid);
    //printintarray(in_edges, num_in_edges_total*2);
    
    if (taskid == 0) { // then its the root node
      nothing_better_array = malloc(numprocs * sizeof(int));
    }
    
    for (i=0; i<N+1; i++) {
      nothing_better = 1; // set it to "True"
      counter = 0;
      // run thru all the outgoing edges
      //checkpoint = 0;
      //printf("taskid %d mark0. in_edges[0]=%d\n", taskid, in_edges[0]);
      edges_for_this_task = 0;
      curtask = whichtask(in_edges[0], vpn, leftover);
      nexttask = curtask;
      for (f=0; f<num_in_edges_total+1; f++) {
        //printf("taskid %d num_in_edges_total=%d\n", taskid, num_in_edges_total);
        if (num_in_edges_total == 0)
          curtask = numprocs; 
        if (f < num_in_edges_total) {
          srcnode = in_edges[f*2];
          destnode = in_edges[f*2 + 1];
          nexttask = whichtask(srcnode, vpn, leftover); // found out to which task this edge leads to
          edgeweight = in_weights[f];
          edge_dest_values[f] = M[destnode-indexoffset];
        } else {
          nexttask = numprocs;
        }
    
        if (nexttask > curtask) { 
            //printf("task %d sending %d scores to task %d.\n", taskid, edges_for_this_task, curtask);
            //printf("Task %d sending Node values to task %d \n", taskid, curtask);
            //printintarray(&incoming_edges[checkpoint*2], edges_for_this_task*2);
            //printdoublearray(&edge_dest_values[counted_in_edges_cumulative[counter]],edges_for_this_task);
            MPI_Isend(&edge_dest_values[counted_in_edges_cumulative[counter]], edges_for_this_task , MPI_DOUBLE, curtask, tag1, MPI_COMM_WORLD, &request);
            edges_for_this_task = 0;
            curtask = nexttask;
            //checkpoint = f;
            counter++;
         
        }
        edges_for_this_task++;
      }
      //printf("taskid %d mark4\n", taskid);
      // now that we're done with all the outgoing edges, time to recieve the incoming ones
      // first, incoming edges from myself
      for (f=0; f<num_edges_to_myself; f++) {
        srcnode = edges_to_myself[f*2];
        destnode = edges_to_myself[f*2 + 1];
        edgeweight = edges_to_myself_weights[f];
        destMindex = destnode - indexoffset;
        srcMindex = srcnode - indexoffset;
        curscore = M[srcMindex];
        otherscore = M[destMindex] + edgeweight;
        if (srcnode == 10) {
          //printf("for srcMindex %d, curscore = %f, M[destMindex] = %f, edgeweights=%f\n", srcMindex, curscore, M[destMindex], edgeweight);
        }
        if (curscore > otherscore) { // then the edge offers a better path
          newM[srcMindex] = otherscore; // change the score
          // ADD THE PATH POINTER
          if (srcnode == 10) {
            //printf("srcnode %d is replacing %f with %f\n", srcnode, curscore, otherscore);
          }
          P[srcMindex] = destnode;
          nothing_better = 0; // something better was found, so we cannot quit early
        }
      }
      // get the incoming edges from other tasks
      //printf("task %d number of outgoing tasks: %d\n", taskid, num_outgoing_tasks);
      counter = 0;
      
      for (f=0; f<counted_out_edges_num_tasks; f++) {
        ontask = counted_out_edges_tasks[f];
        index = counted_out_edges_cumulative[f];
        size = counted_out_edges_blocked[f];
        //printf("task %d size: %d.\n", taskid, size);
        //printf("task %d recieving %d edges values at location %d from task %d\n",taskid, outgoing_num_edges[counter], index,  ontask);
        //MPI_Irecv(&outgoing_edge_values[index], outgoing_num_edges[f], MPI_DOUBLE, ontask, tag1, MPI_COMM_WORLD, &requestarray[counter]);
        MPI_Irecv(&out_edge_values[index], size, MPI_DOUBLE, ontask, tag1, MPI_COMM_WORLD, &requestarray[f]);
        //printf("task %d recieved this from task %d:", taskid, ontask);
        //printdoublearray(&out_edge_values[index], size);
      }
      MPI_Waitall(counted_out_edges_num_tasks, &requestarray[0], &statusarray[0]);
      //printf("Outgoing_edge_values for task %d:", taskid);
      //printdoublearray(out_edge_values, num_out_edges_total);
    
      counter=0; 
      for (f=0; f<num_out_edges_total; f++) {
        srcnode = out_edges[f*2]; 
        destnode = out_edges[f*2 + 1];
        if (taskid == whichtask(destnode, vpn, leftover))
          continue; // if this edge points inside the task, then skip it
        edgeweight = out_weights[f];
        destMindex = destnode - indexoffset;
        srcMindex = srcnode - indexoffset;
        curscore = M[srcMindex];
        otherscore = out_edge_values[f] + edgeweight;
        if (curscore > otherscore) { // then the new edge offers a better path
          newM[srcMindex] = otherscore;
          P[srcMindex] = destnode; // assign the best pointer 
          // ADD the path pointer
          nothing_better = 0; // something better was found so we cannot quit early
        }
        counter++;
      }
      // CHECK TO SEE IF ANYTHING HAS CHANGED IN THE GRAPH, if not, then send to the other tasks that nothing has happened. If nothing has happened in any of them, then we have found the best path and can quit early
      // send whether anything has changed to task 0
      nothing_better_reduced=0;
      MPI_Reduce(&nothing_better, &nothing_better_reduced, 1, MPI_INT, MPI_MIN, 0, MPI_COMM_WORLD);
      if (taskid == 0) {
        //printf("REDUCTION RESULTS: %d\n", nothing_better_reduced);
        if (nothing_better_reduced == 1) { // then every single one of the tasks had nothing better to refine, the refinement is over
          //printf("nothing better was found in any task. Ending the refinement. \n");
          //break;
        }
      }
      MPI_Bcast(&nothing_better_reduced, 1, MPI_INT, 0, MPI_COMM_WORLD);
      
      if (nothing_better_reduced == 1) { // then nothing better has been found in any task
        // send a message around that nothing better was found and we can quit
        //printf("Nothing better was found in task %d\n", taskid);
        break;
      }
      //printf("task %d M after iteration %d ", taskid,i);
      //printdoublearray(&M[0],vpn2);
      //printintarray(&P[0], vpn2);
      //printdoublearray(&newM[0],vpn2);
      // Detect negative cycle
      memsize = vpn2 * sizeof(double);
      memcpy(&M[0], &newM[0], memsize);
    } 
    
    // the last two iterations, check to make sure the solution has converged, if not, then we have a negative cycle
    if (whichtask(start_vertex, vpn, leftover) == taskid) {
      //printf("Best path length=%f\n",  M[start_vertex - indexoffset]);
      best_path_length = M[start_vertex - indexoffset];
      MPI_Isend(&best_path_length, 1, MPI_DOUBLE, MASTER, tag3, MPI_COMM_WORLD, &request);
    }
    
    if (taskid == MASTER) {
      MPI_Recv(&best_path_length, 1, MPI_DOUBLE, whichtask(start_vertex, vpn, leftover), tag3, MPI_COMM_WORLD, &status);
      if (isfinite(best_path_length) == 0) {
        // then we have a disconnected graph
        printf("Alert: No optimal path found. No paths exist from specified start node to target node.\n");
      }
      if (nothing_better_reduced == 0) {
        best_path_length = HUGE_VAL;
        printf("NEGATIVE CYCLE DETECTED\n");
      }
    }
    
    MPI_Bcast(&best_path_length, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    
    endtime = MPI_Wtime();
    if (taskid == whichtask(start_vertex, vpn, leftover))
      printf("refinement time: %f\n", endtime-starttime);
    
    // The refinement is over, now we need to walk thru the path until we reach the
    // destination node, sending the root node the optimal path
    //printf("taskid %d mark10\n", taskid);
    starttime = MPI_Wtime();
    int onnode = start_vertex; // always start here
    int nextnode;
    int Path_counter=0;
    int Path[vpn2]; // this will contain the actual path
    int task_who_has_onnode;
    int send_buffer[2];
    int recv_buffer[2];
    int len_path_so_far = 0;
    int path_piece_length;
    int *path_piece;
    int testvar;
    int prev_path_loc = 0;
    counter = 0;
    
    if (taskid == 0)
      path_piece = malloc(N * sizeof(int));
    
    while (Path_counter <= N) {
      if ( isfinite(best_path_length) == 0)
        break;
      task_who_has_onnode = whichtask(onnode, vpn, leftover);
      if (taskid == task_who_has_onnode) {
        while (taskid == whichtask(onnode, vpn, leftover)) { // then we have the current node
          Path[counter] = onnode;
          Path_counter++;
          counter++;
          nextnode = P[onnode - indexoffset];
          if (taskid != whichtask(nextnode, vpn, leftover) && nextnode != finish_vertex) { // then we will be in another node next time
            //printf("task %d is sending this partial path of length %d to master task:", taskid, counter);
            //printintarray(&Path[0], counter);
            if (taskid == MASTER) {
              path_piece_length = counter - prev_path_loc;
              memsize = path_piece_length * sizeof(int);
              memcpy(&path_piece[len_path_so_far], &Path[prev_path_loc], memsize);
              len_path_so_far += path_piece_length;
              prev_path_loc = len_path_so_far;
            } else {
              MPI_Isend(&counter, 1, MPI_INT, MASTER, 0, MPI_COMM_WORLD, &requestarray[0]);
              MPI_Isend(&Path[0], counter, MPI_INT, MASTER, tag1, MPI_COMM_WORLD, &requestarray[1]);
            }
          }
          if (Path_counter > N) { // then we have a negative cycle
            printf("NEGATIVE CYCLE DETECTED\n");
            if (taskid == MASTER) {
              path_piece_length = counter;
              memsize = path_piece_length * sizeof(int);
              memcpy(&path_piece[len_path_so_far], &Path[0], memsize);
              len_path_so_far += path_piece_length;
            } else {
              MPI_Isend(&counter, 1, MPI_INT, MASTER, 0, MPI_COMM_WORLD, &requestarray[0]);
              MPI_Isend(&Path[0], counter, MPI_INT, MASTER, tag1, MPI_COMM_WORLD, &requestarray[1]);
            }
            break;
          }
          if (nextnode == finish_vertex) { // then we've found the path to the end!
            //printf("task %d is sending this partial path of length %d to master task:", taskid, counter);
            //printintarray(&Path[0], counter);
            //printf("full path found");
            Path[counter] = nextnode;
            counter++; // its important that this occurs here so that the master task will also be sent the destination node
            //printintarray(&Path[0], counter);
            onnode = -1;
            if (taskid == MASTER) {
              path_piece_length = counter - prev_path_loc;
              memsize = path_piece_length * sizeof(int);
              memcpy(&path_piece[len_path_so_far], &Path[prev_path_loc], memsize);
              len_path_so_far += path_piece_length;
            } else {
              MPI_Isend(&counter, 1, MPI_INT, MASTER, 0, MPI_COMM_WORLD, &requestarray[0]);
              MPI_Isend(&Path[0], counter, MPI_INT, MASTER, tag1, MPI_COMM_WORLD, &requestarray[1]);
            }
            break;
          }
      
          //printf("onnode = %d, nextnode = %d\n", onnode, nextnode);
          onnode = nextnode;
        }
        send_buffer[0] = onnode;
        send_buffer[1] = Path_counter;
        MPI_Bcast(&send_buffer[0], 2, MPI_INT, taskid, MPI_COMM_WORLD);
    
      } else {
        MPI_Bcast(&recv_buffer[0], 2, MPI_INT, task_who_has_onnode, MPI_COMM_WORLD);
        onnode = recv_buffer[0];
        Path_counter = recv_buffer[1];
    
      }
      if (taskid == MASTER && task_who_has_onnode != MASTER) { // the master task needs to recieve each piece of the path in order to put it together
        //MPI_Waitall(2, &requestarray[0], &statusarray[0]);
        //printf("MASTER waiting to recieve paths from task %d\n", task_who_has_onnode);
        MPI_Recv(&path_piece_length, 1, MPI_INT, task_who_has_onnode, 0, MPI_COMM_WORLD, &status);
        //printf("MASTER recieved path piece of length %d from task %d in memory location %d\n", path_piece_length, task_who_has_onnode, len_path_so_far);
        MPI_Recv(&path_piece[len_path_so_far], path_piece_length, MPI_INT, task_who_has_onnode, tag1, MPI_COMM_WORLD, &status);
        //printf("MASTER path_piece[0] = %d\n", path_piece);
        len_path_so_far += path_piece_length;
      }
      if (onnode == -1) { // then the destination has been reached
        //printf("taskid %d discovered that destination is reached\n", taskid);
        break;
      }
    }
    //MPI_Barrier(MPI_COMM_WORLD);
    //printf("taskid %d mark 20\n", taskid);
    if (taskid == 0) {
      printf("Optimal path of length %f:  ", best_path_length);
      printintarray(path_piece, len_path_so_far);
    }
    
    endtime = MPI_Wtime();
    if (taskid == whichtask(0, vpn, leftover))
      printf("traversal time: %f\n", endtime-starttime);
    
    free(out_edges);
    free(out_weights);
    /*
    if (taskid == 2) {
      printf("inedges for taskid %d:", taskid);
      printintarray(in_edges, num_in_edges_total);
    }*/
    //printf("taskid %d mark 22\n", taskid);
    free(in_edges);
    //printf("taskid %d mark 23\n", taskid);
    free(in_weights);
    //printf("taskid %d mark 24\n", taskid);
    free(edges_to_myself);
    
    //printf("taskid %d mark 25\n", taskid);
    free(edges_to_myself_weights);
    //free(incoming_weights);
    free(out_edge_values);
    //free(M);
    if (taskid == 0) {
      free(nothing_better_array);
      free(path_piece);
    
    }
    MPI_Finalize();
    
    //printf("taskid %d mark 99\n", taskid);
    return(0);
    }
    /*
    /*********************************
    FILE: bellmanford1.c
    DESCRIPTION:
    Final project for parallel class.
    This project is a parallel implementation of the Bellman Ford algorithm for finding
    the shortest path in a graph with negative path lengths, and also for finding
    negative path cycles.
    In this first version, the graph topology is not used for the sake of simplicity
    
    AUTHOR: Lane Votapka
    LAST REVISED: May 3, 2012
    ********************************
    #include <mpi.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>
    
    #define MASTER 0
    #define INF 9999999.9
    
    int whichtask(int node, int chunk, int leftover_nodes) {
      int tasknum;
      tasknum = node / chunk;
      if ((tasknum != 0) && (tasknum-1 < leftover_nodes) && (node % chunk == 0)) {
        tasknum--;
      }
      return tasknum;
    }
    
    int sort_by_destination(int *edge, int total_edges) {
      // The input to this algorithm is an array of pairs, the array is sorted by the second member of the pair
      // solution: mergesort
      int i;
      for (i=0; i<total_edges; i+=2) {
    
      // return the address of the new list
    }
    
    int quicksort(int *our_array, int array_len) {
      int pivot;
      int pivot_loc = array_len/2;
      int i, greater_index = 0, less_index = 0;
      if (array_len <= 1) { // an array of length 0 or 1 is already sorted
        return &our_array;
      }
      pivot = our_array[pivot_loc]; // choose a pivot halfway in
      int less_len = (array_len/2);
      int greater_len = (array_len - (array_len/2));
      int less[array_len];
      int greater[array_len];
      for (i=0; i<array_len; i++) {
        if (i == pivol_loc) {
          continue;
        } else if (our_array[i] <= pivot) {
          // then append x to less
          less[less_index] = our_array[i]; // copy the pivot to the end of the less array
          less_index++; 
        } else {
          // then append x to greater
          greater[greater_index] = our_array[i];
          greater_index++;
        }
        quicksort(&less, less_index);
        quicksort(&greater, greater_index);
        // now copy the memory to the corresponding locations
        memcpy(our_array, less, less_index);
        our_array[less_index] = pivot;
        memcpy(our_array+less_index+1, greater, greater_index);
      }
    }
    
    int main (int argc, char* argv[]) {
    
    printf("whichtask: %d", whichtask(4, 5, 4));
    
    int numtasks, taskid, rc, dest, offset, i, f, tag1=1, tag2=1, source, chunk, leftover_nodes;
    int desttask;
    int N = 10; // number of nodes in the graph, it's set to 10 for testing, is overwritten by file
    int E; // number of edges in the graph
    int assigned_num_nodes;
    int num_nodes_sending_edges;
    double *assigned_nodes;
    // Initializations
    
    MPI_Status status; // MPI status structure
    MPI_Request request; // MPI request structurei
    MPI_Request request1;
    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &numtasks); // how many of us are there?
    MPI_Comm_rank(MPI_COMM_WORLD, &taskid); // who am I?
    
    double testline[10] = { 1.0, INF, 1.0, 1.0, INF, 1.0, 1.0, INF, 1.0, INF };
    // 1. The graph must be parsed from an input file
    
    // read N
    chunk = N / numtasks;
    leftover_nodes = N % numtasks;
    assigned_nodes = malloc(N * (chunk+1) * sizeof(double)); // need to make this piece of memory big enough to handle anything sent to it
    //printf("Task %d now allocating %d space for memory in location: %x\n", taskid, (N * (chunk+1) * sizeof(double)), &assigned_nodes);
    if (taskid == MASTER) {
      for (desttask=0; desttask<numtasks; desttask++) { // for all other tasks
        if (desttask < leftover_nodes) { // then we need to assign one extra to this task
          assigned_num_nodes = chunk + 1;
        } else { 
          assigned_num_nodes = chunk; 
        }
        // read chunk lines from the file
            
        for ( i=0; i<assigned_num_nodes; i++ ) {
          // edge information  = { whatever was in the file }
          //nodeline = testline;
          memcpy(&assigned_nodes[N*i], testline, N*sizeof(double)); // copying the edge weights to one big array to be sent to other tasks
          //for (f=0;f<N;f++)
            //printf("%f,", assigned_nodes[f]);
        }
          //printf("master node now sending to task: %d. Amount of memory: %d\n", desttask, (N*assigned_num_nodes*sizeof(double)));
          MPI_Isend(&assigned_num_nodes, 1, MPI_INT, desttask, 0, MPI_COMM_WORLD, &request); // tell the worker how many nodes to expect
          MPI_Isend(assigned_nodes, N*assigned_num_nodes, MPI_DOUBLE, desttask, 0, MPI_COMM_WORLD, &request1);  // sending edge information
      }
    }
    // } else { // then I'm a worker. NOTE: _else_ may not be necessary
      MPI_Irecv(&assigned_num_nodes, 1, MPI_INT, MASTER, 0, MPI_COMM_WORLD, &request);
      MPI_Wait(&request, &status); // wait until we have the number of nodes for this task
      //printf("Task %d recieved %d nodes. Set to recieve %d amount of memory\n", taskid, assigned_num_nodes, (N*assigned_num_nodes*sizeof(double*))); // make sure that our task has recieved its assigned nodes and all
      //printf("address of &assigned_nodes: %x\n", &assigned_nodes);
      MPI_Irecv(assigned_nodes, N*assigned_num_nodes, MPI_DOUBLE, MASTER, 0, MPI_COMM_WORLD, &request1);
      // unpack all the edge information
      MPI_Wait(&request1, &status);
      /*printf("Task %d recieved info: ", taskid);
      for (i = 0; i<(N*assigned_num_nodes); i++) {
        printf("%f,", assigned_nodes[i]);
      }
      printf("\n");
      *
      int out_edge[assigned_num_nodes*N*2]; //even indeces; node from. Odd indeces; node to
      double out_weight[assigned_num_nodes*N]; // weights corresponding to above index divided by 2
      int on_edge = 0;
      double weight_for_node_f;
      int total_outgoing_edges;
      for (i=0; i<assigned_num_nodes; i++) { // for every node i in task
        for (f=0; f<N; f++) { // for every other node in the graph, edge or not
          weight_for_node_f = assigned_nodes[(i*N)+f];
          if (weight_for_node_f != INF) {
            out_edge[on_edge * 2] = i;
    	out_edge[on_edge * 2 + 1] = f;
    	out_weight[on_edge] = weight_for_node_f;
            on_edge++;
          }
        }
      }
      total_outgoing_edges = on_edge;
      int *out_edge_sorted;
      // sort the out_edges by destination index
      out_edge_sorted = sort_by_destination(&out_edge, total_outgoing_edges);
      int destnode, srcnode, edges_in_task, curtask, oldtask;
      int edgebuffer[total_outgoing_edges*2];
      double weightbuffer[total_outgoing_edges];
      for (i=0; i<total_outgoing_edges*2; i+=2) {
        destnode = out_edge_sorted[i+1]; // find the task node [i] is in.
        srcnode = out_edge_sorted[i];
        curtask = whichtask(destnode, chunk, leftover_nodes); // find whichever task the destnode belongs to
        if (curtask > oldtask) { // then its a new task
          // send all the old information
          MPI_Isend(&edges_in_task, 1, MPI_INT, oldtask, 0, MPI_COMM_WORLD, &request); // send however many incoming nodes will be recieved
          MPI_Isend(&edgebuffer, edges_in_task*2, MPI_INT, oldtask, 1, MPI_COMM_WORLD, &request1); // send the buffer containing the edges 
          MPI_Isend(&weightbuffer, edges_in_task, MPI_DOUBLE, oldtask, 2, MPI_COMM_WORLD, &request);
          edges_in_task = 0;
        }
        oldtask = curtask;
      // once sorted by destination edges, run through every destination in its respective task, once we reach a new task
      //   then lump everything together so far and send away to the task we just finished
      /*
      int num_outgoing_edges[assigned_num_nodes]; // for this task
      int outgoing_edge_weight_index[assigned_num_nodes]; // the index in the outgoing edge array for node i
      double outgoing_edge_weight[N*assigned_num_nodes]; // contains the actual edge weights
      int outgoing_edge_destnode [N*assigned_num_nodes]; // the node to which this edge is going
      double weight_for_node_f;
      for (i=0;i<assigned_num_nodes;i++) { // every node in task
        num_outgoing_edges[i] = 0;
        if (i == 0) {
          outgoing_edge_weight_index[i] = 0;
        } else {
          outgoing_edge_weight_index[i] = outgoing_edge_weight_index[i-1] + num_outgoing_edges[i-1]; 
        }
        for (f=0; f<N; f++) { // for each other node
          weight_for_node_f = assigned_nodes[(i*N)+f];
          if (weight_for_node_f != INF) {
            num_outgoing_edges[i]++;
    	// append the edge weight to the outgoing_edge_weight array
    	outgoing_edge_weight[outgoing_edge_weight_index[i] + num_outgoing_edges[i]-1] = weight_for_node_f;
    	outgoing_edge_destnode[outgoing_edge_weight_index[i] + num_outgoing_edges[i]-1] = f;
          }
        }
        // now we know how many edges are coming out of i
      }
      printf("outgoing_edge_destnode: ");
      for (i=0;i<6;i++) printf("%d,", outgoing_edge_destnode[i]);
      printf("\n");
      // send all information to the nodes to which the edges point
      for (i=0;i<assigned_num_nodes;i++) { // for every node in this task
        for (f=0;f<num_outgoing_edges[i];f++) { // for every edge going out from this node
          
        }
      }
      // wait for all this to happen
      int from_task; // whichever task a node belongs to
      int total_incoming_edges = 0; // the total number of incoming edges into this node 
      int num_incoming_edges[N]; // an array of the number of incoming edges from all nodes
      int my_num_incoming_edges; // a temporary variable
      for (i=0; i<N; i++) { // for each node
        // need to figure out which task this node belongs to
        //from_task = whichtask(i);
    
        //listen for an incoming edge
        //MPI_Irecv(&my_num_incoming_edges, 1, MPI_INT, i, 0, MPI_COMM_WORLD, &request);
        //total_incoming_edges += my_num_incoming_edges;
        //num_incoming_edges[i] = my_num_incoming_edges;
      }
      
      // allocate memory equal to the number of edges coming in
      int incoming_edge_weight[total_incoming_edges];  
      // recieve incoming edge information
      for (i=0;i<total_incoming_edges; i++) {
        // something
      }
      *
    // Finalize and free all memory allocations
    MPI_Finalize();
    free(assigned_nodes); // free up this allocation
    return(0);
    }
    
    
    */
    
    

`
