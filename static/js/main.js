var canvases = [];
var currentCanvasIndex = 0;


function newCanvas(newIndex){  
   
  console.log("New Canvas index#"+newIndex);
  
  let canvas = new fabric.Canvas('canvas-element-' + newIndex);
  fabric.Object.prototype.transparentCorners = false;

  let t = new fabric.IText('CANVAS#'+(newIndex+1), {
    top: 10,
    left: 10,
    fontSize: 15,
  });
      
  canvas.add(t);
  canvas.renderAll();
  
  let sampleImg = 'https://www.printobe.com/wp-content/uploads/2019/07/logo_Printobe.png';
  fabric.Image.fromURL(sampleImg, function(img) {
    
      img.set({
        scaleX: 0.2,
        scaleY: 0.2,
        top: 50,
        left: 0
      });
    
      canvas.add(img);
      canvas.renderAll();
  });
  
  canvases[newIndex] = canvas;
  bindCanvas(canvas);
  
  
}

function cloneCanvas(sourceIndex, newIndex){
   
  console.log("index#"+sourceIndex+" > index#"+newIndex);
  
  let canvas = new fabric.Canvas('canvas-element-' + newIndex);
  
  canvas.loadFromJSON(
        JSON.stringify(canvases[sourceIndex]), 
        function(){       
            canvas.renderAll();
        }
  ); 
  
  canvases[newIndex] = canvas;
  bindCanvas(canvas);
  
    
}
  
function bindCanvas(canvas){
  
    canvas.on('selection:created', function(o){
  
    console.log('selection:created');
    let canvasId = o.target.canvas.getElement().id;
    
    for(let i=0; i < canvases.length; i++){
      if(canvases[i] == o.target.canvas){
        currentCanvasIndex = i;        
      }else{
        console.log(canvases[i].getElement().id);
        //console.log(canvases[i]);
        canvases[i].discardActiveObject().renderAll();
      }
    }
        
  });
  
}





jQuery(function(){
  
  newCanvas(0);
  
  $('#stage').on('click', '.add-canvas', function(){
  
    console.log('add-canvas');
    
    let newIndex = canvases.length;
    
    let $canvaWrapper = $("<div>");
    $canvaWrapper.addClass("canvas-wrapper");    
    $canvaWrapper.attr("data-index", newIndex);  
    
    let $canva = $("<canvas>");
    $canva.attr({ width: 600, height: 450});
    $canva.css( "display", "none" );
    $canva.attr( "id", "canvas-element-" + newIndex );
    
    let $btnRemove = $('<button class="remove-canvas">');
    $btnRemove.append('<i class="fa fa-times">');
     
    let $btnClone = $('<button class="clone-canvas">');
    $btnClone.append('<i class="fa fa-clone">');
    
    $canvaWrapper.append($canva);
    $canvaWrapper.append($btnRemove);
    $canvaWrapper.append($btnClone);

    $canvaWrapper.insertBefore('.add-canvas');
    
    $canva.fadeIn( "fast", function(){
      
      newCanvas(newIndex);
      
    });
    

       
  });
      
  $('#stage').on('click', '.remove-canvas', function(){
         
      let index = parseInt($(this).parents(".canvas-wrapper").attr("data-index"));
    
      console.log("remove-canvas: index#"+index);
         
      //console.log(canvases);
    
      $(this).parents(".canvas-wrapper").hide();
      
      delete canvases[index];

    
    });
  
  $('#stage').on('click', '.clone-canvas', function(){ 
      
      console.log('clone-canvas');
    
      let index = parseInt($(this).parents(".canvas-wrapper").attr("data-index"));
      
     
      let newIndex = index+1;
    
      let $canvaWrapper = $("<div>");
      $canvaWrapper.addClass("canvas-wrapper");    
      $canvaWrapper.attr("data-index", newIndex);  

      let $canva = $("<canvas>");
      $canva.attr({ width: 600, height: 450});
      $canva.css( "display", "none" );
      $canva.attr( "id", "canvas-element-" + newIndex );

      let $btnRemove = $('<button class="remove-canvas">');
      $btnRemove.append('<i class="fa fa-times">');

      let $btnClone = $('<button class="clone-canvas">');
      $btnClone.append('<i class="fa fa-clone">');
    
      $canvaWrapper.append($canva);
      $canvaWrapper.append($btnRemove);
      $canvaWrapper.append($btnClone);

      $canvaWrapper.insertBefore(".add-canvas");
      $canva.fadeIn( "fast", function(){

        cloneCanvas(index, newIndex);

      });
      
      
    });
  
  
});