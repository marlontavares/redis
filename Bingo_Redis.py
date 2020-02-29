#!/usr/bin/env python
# coding: utf-8

# In[1]:


import redis


# In[2]:


redis = redis.Redis('localhost')


# In[3]:


# cria lista de numeros para cartelas
def cria_lista():
    for x in range(99):
        redis.sadd("lista", x+1)


# In[4]:


# cadastra os jogadores
ctx = 1
while ctx <= 50:
    i = str(ctx)
    redis.hset("user"+i, "nome", "user"+i)
    redis.hset("user"+i, "cartela", "cartela"+i)
    redis.hset("user"+i, "score", "score"+i)
    
    ctx += 1


# In[5]:


# cria as cartelas
for x in range(50):
    cria_lista()
    for i in range(15):
        num = redis.srandmember('lista')
        redis.sadd("cartela"+str(x+1), num)
        redis.srem('lista', num)


# In[6]:


# cria score zero para todos
for x in range(50):
    redis.zadd("score", {"score"+str(x+1): 0})


# In[7]:


#sorteia os numeros até alguem chegue ao score 15
cria_lista()
i = 0
while i != 1:  
    num = redis.srandmember('lista')
    redis.srem('lista', num)
    
    for x in range(50):
        ctl = 'cartela'+str(x+1)
        scr = 'score'+str(x+1)
        nm = 'user'+str(x+1)
        if redis.sismember(ctl,num):
            redis.zincrby('score', float(1), scr)
            
        if len(redis.zrangebyscore('score',15,15)) > 0:
            i = 1
    


# In[20]:


#jogadores que alcançaram 15 pontos
ganhadores = redis.zrangebyscore('score',15,15)
print(redis.zrangebyscore('score',15,15))


# In[21]:


#busca o nome dos jogadores com 15 pontos
for x in range(50):
    for i in ganhadores:
        if redis.hget('user'+str(x+1), 'score') == i:
            print(redis.hget('user'+str(x+1), 'nome'))


# In[ ]:




